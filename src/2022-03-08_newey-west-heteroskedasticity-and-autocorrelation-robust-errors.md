Modeling autocorrelations: Newey-West HAC and ARIMA modeling
================
Nayef Ahmad
2022-03-08

-   [1 Overview](#overview)
-   [2 Libraries](#libraries)
-   [3 Functions](#functions)
-   [4 Data generation](#data-generation)
    -   [4.1 White noise error](#white-noise-error)
-   [5 Example 1: White noise error (base
    case)](#example-1-white-noise-error-base-case)
-   [6 Example 2: Autocorrelated error](#example-2-autocorrelated-error)
-   [7 Example 3: Pure ARIMA series as dependent
    variable](#example-3-pure-arima-series-as-dependent-variable)

# 1 Overview

When there is autocorrelation of residuals, this means that your model
is leaving value on the table - out of sheer laziness, it has not
accounted for all of the structure available. You should not want to
listen to the advice of someone who does not work as hard as you do. Ask
them to work harder and come back to you after they’ve done their
homework. Then you can discuss results (i.e. make inferences).

In this file, we explore two ways to get your model to “work harder” and
account for autocorrelation. The first is to use OLS as usual, then
correct the estimate of the covariance matrix of the parameters. The
second is to directly model autocorrelation using an ARIMA model.

**References:**

-   [Cross Validated - OLS regression with Newey-West error
    term](https://stats.stackexchange.com/a/254596/56828). This includes
    a simulation of autocorrelated residuals, and compares ordinary OLS
    vs HAC inferences.
-   [Cross Validated - two ways of dealing with the problem of
    autocorrelated
    errors](https://stats.stackexchange.com/a/181297/56828). This argues
    that the ARIMA approach is better than using OLS + HAC errors.

# 2 Libraries

``` r
library(lmtest)
```

    ## Warning: package 'lmtest' was built under R version 4.0.5

    ## Loading required package: zoo

    ## Warning: package 'zoo' was built under R version 4.0.3

    ## 
    ## Attaching package: 'zoo'

    ## The following objects are masked from 'package:base':
    ## 
    ##     as.Date, as.Date.numeric

``` r
library(sandwich)
```

    ## Warning: package 'sandwich' was built under R version 4.0.5

``` r
library(forecast)
```

    ## Warning: package 'forecast' was built under R version 4.0.5

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

``` r
library(tidyverse)
```

    ## Warning: package 'tidyverse' was built under R version 4.0.3

    ## -- Attaching packages --------------------------------------- tidyverse 1.3.0 --

    ## v ggplot2 3.3.5     v purrr   0.3.4
    ## v tibble  3.0.6     v dplyr   1.0.3
    ## v tidyr   1.1.2     v stringr 1.4.0
    ## v readr   1.4.0     v forcats 0.5.1

    ## Warning: package 'ggplot2' was built under R version 4.0.5

    ## Warning: package 'tibble' was built under R version 4.0.3

    ## Warning: package 'tidyr' was built under R version 4.0.3

    ## Warning: package 'readr' was built under R version 4.0.3

    ## Warning: package 'purrr' was built under R version 4.0.3

    ## Warning: package 'dplyr' was built under R version 4.0.3

    ## Warning: package 'stringr' was built under R version 4.0.3

    ## Warning: package 'forcats' was built under R version 4.0.3

    ## -- Conflicts ------------------------------------------ tidyverse_conflicts() --
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

``` r
par(mfrow = c(1,3))

layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)
# layout.show(3)
```

# 3 Functions

``` r
data_with_white_noise_error <- function(iterations = 20, 
                                        n = 50){
  # Create a dataframe of simulated X and Y data, for a given sample size.
  # Each iteration is a single sample of size n for the given parameters.  
  # We want several samples for each set of parameters. 
  # 
  # Args:
  #   - iterations: number of datasets to create 
  # 
  # Returns: 
  #   - df: dataframe with columns x and y
  
  slope <- .05 
  
  white_noise_residuals <- rnorm(n * iterations)
  x <- rep(seq(n), iterations)
  y <- slope * x + white_noise_residuals
    
  sample_id <- rep(seq(1:iterations), each = n)
    
  
  df <- data.frame(sample_id, x , y)
  
  return(df)
  
}






get_slope_line_vector_from_arima <- function(arima_model_fitted){
  # Args: 
  # - arima_model_fitted: Fitted ARIMA model, such as the models returned 
  #     by forecast::auto.arima()
  # 
  # Returns: 
  # - line_vector: A numeric vector of same length as the data passed to 
  #     the ARIMA fitting procedure. These values represent the underlying 
  #     linear trend after fitting the ARIMA model 
  
  if (is.na(arima_model_fitted$coef["intercept"])) {
    intercept <- 0
  } else {
    intercept <- arima_model_fitted$coef["intercept"]
  }
  
  if (is.na(arima_model_fitted$coef["xreg"])) {
    slope <- 0
  } else {
    slope <- arima_model_fitted$coef["xreg"]
  }
  
  line_vector <- 
    intercept + slope * c(1:arima_model_fitted$nobs)
  
  return(line_vector)
}
```

# 4 Data generation

Let’s visualize what these series look like, for a given n value.

## 4.1 White noise error

``` r
seed <- 2022
set.seed(seed)

df <- data_with_white_noise_error(iterations = 20)

df %>% 
  ggplot(aes(x = x, y = y, group = sample_id)) + 
  geom_line(alpha=.5) + 
  facet_wrap(~sample_id) + 
  theme_minimal()
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

Now let’s collect several different sample sizes into dataframes.

``` r
# df_white_noise <- multiple_n_white_noise_error(iterations = i, n_values = c(50, 100)


# multiple_n_white_noise_error: 
#   - for loops over n_values, calls data_with_white_noise_error()
#   - collects all series, does group_by(n, iteration_num, ar_coef) %>% cur_group_id() 



# df_arima_error <- data_with_arima_error(iterations = i, n = 50, ar_coeffecients = seq(0, .9, .2))

# df_arima <- data_with_arima_response(iterations = i, n = 50, ar_coeffecients = seq(0, .9, .2))
```

# 5 Example 1: White noise error (base case)

First set up the data.

``` r
n <- 50
slope <- .05


white_noise_residuals <- rnorm(n)
x <- 1:n
y <- slope*(x) + white_noise_residuals
```

Fit lm model, and plot.

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)


fit <- lm(y~x)

plot(x,y)
abline(fit, col = 'blue')
acf(fit$residuals)
pacf(fit$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

Model output, using standard and Newey-West HAC errors:

``` r
summary(fit) # standard estimates
```

    ## 
    ## Call:
    ## lm(formula = y ~ x)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -3.05902 -0.70452  0.06119  0.74459  2.80218 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  0.35407    0.33548   1.055 0.296527    
    ## x            0.04304    0.01145   3.759 0.000463 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 1.168 on 48 degrees of freedom
    ## Multiple R-squared:  0.2274, Adjusted R-squared:  0.2113 
    ## F-statistic: 14.13 on 1 and 48 DF,  p-value: 0.0004626

``` r
coeftest(fit, vcov = NeweyWest(fit, verbose = T))
```

    ## 
    ## Lag truncation parameter chosen: 1

    ## 
    ## t test of coefficients:
    ## 
    ##             Estimate Std. Error t value  Pr(>|t|)    
    ## (Intercept) 0.354065   0.322398  1.0982 0.2775852    
    ## x           0.043042   0.010292  4.1820 0.0001219 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Fit ARIMA model, and plot

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)

fit_arima <- auto.arima(y, xreg = x)

plot(x,y)
lines(fit_arima$fitted, col = "blue")
lines(get_slope_line_vector_from_arima(fit_arima), col = "darkgreen")
acf(fit_arima$residuals)
pacf(fit_arima$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

ARIMA model output:

``` r
summary(fit_arima)
```

    ## Series: y 
    ## Regression with ARIMA(0,0,0) errors 
    ## 
    ## Coefficients:
    ##         xreg
    ##       0.0536
    ## s.e.  0.0056
    ## 
    ## sigma^2 = 1.368:  log likelihood = -78.28
    ## AIC=160.56   AICc=160.81   BIC=164.38
    ## 
    ## Training set error measures:
    ##                      ME     RMSE       MAE       MPE     MAPE      MASE
    ## Training set 0.08588708 1.157955 0.9312607 -31.03914 104.8873 0.7075574
    ##                      ACF1
    ## Training set -0.006382735

# 6 Example 2: Autocorrelated error

In cases where non-arima fit gives almost same estimate as arima fit,
but p-value of t-test for coefficient is far from significant, I would
prefer the arima fit.

-   Examples where Arima fit is better than OLS:
    -   seed 1, 2, 4, 5, 10, 13, 16, 17, 20
-   Examples where Arima fit is better than OLS + HAC:
    -   seed 1, 2, 4, 5, 10, 12, 13, 14, 15, 16, 17, 19, 20
-   Examples where no benefit to Arima:
    -   seed 3, 6, 7, 8, 9, 11, 18

First set up the data.

``` r
seed <- 2
set.seed(seed)

n <- 50
slope <- .05


correlated_residuals <- arima.sim(list(ar = .9), n)
x <- 1:n
y <- slope*(x) + correlated_residuals
```

Fit lm model, and plot.

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)

fit <- lm(y~x)

plot(x,y)
abline(fit, col = 'blue')
acf(fit$residuals)
pacf(fit$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-11-1.png)<!-- -->

Model output, using standard and Newey-West HAC errors:

``` r
summary(fit) # standard estimates
```

    ## 
    ## Call:
    ## lm(formula = y ~ x)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -3.6238 -1.2741 -0.1119  1.1357  4.3991 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)  
    ## (Intercept) -0.46224    0.46547  -0.993   0.3257  
    ## x            0.02811    0.01589   1.769   0.0832 .
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 1.621 on 48 degrees of freedom
    ## Multiple R-squared:  0.06123,    Adjusted R-squared:  0.04168 
    ## F-statistic: 3.131 on 1 and 48 DF,  p-value: 0.08317

``` r
coeftest(fit, vcov = NeweyWest(fit, verbose = T))
```

    ## 
    ## Lag truncation parameter chosen: 1

    ## 
    ## t test of coefficients:
    ## 
    ##             Estimate Std. Error t value Pr(>|t|)
    ## (Intercept) -0.46224    4.57966 -0.1009   0.9200
    ## x            0.02811    0.23621  0.1190   0.9058

Fit ARIMA model, and plot

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)

fit_arima <- auto.arima(y, xreg = x)
summary(fit_arima)
```

    ## Series: y 
    ## Regression with ARIMA(1,0,0) errors 
    ## 
    ## Coefficients:
    ##          ar1    xreg
    ##       0.7457  0.0287
    ## s.e.  0.1060  0.0213
    ## 
    ## sigma^2 = 1.381:  log likelihood = -78.39
    ## AIC=162.79   AICc=163.31   BIC=168.52
    ## 
    ## Training set error measures:
    ##                       ME     RMSE       MAE       MPE    MAPE      MASE
    ## Training set -0.06508041 1.151214 0.9707687 -66.25045 195.649 0.9561247
    ##                    ACF1
    ## Training set 0.05940882

``` r
plot(x,y)
lines(fit_arima$fitted, col = "blue")
lines(get_slope_line_vector_from_arima(fit_arima), col = "darkgreen")
acf(fit_arima$residuals)
pacf(fit_arima$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-13-1.png)<!-- -->

In this specific example, where `seed =` 2, we can see that the OLS fit
and the (OLS + HAC) fit find the estimate a slope value close to the
true value of 0.05, but because of the large amount of unexplained
structure, inference is not valid - the slope coefficient is not
significant.

On the other hand, the ARIMA fit includes the slope, and the estimate is
relatively close to the true value.

# 7 Example 3: Pure ARIMA series as dependent variable

First set up the data.

``` r
seed <- 3
set.seed(seed)

n <- 50
slope <- .05


y <- arima.sim(list(ar = .9), n)
x <- 1:n
```

Fit lm model, and plot.

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)

fit <- lm(y~x)

plot(x,y)
abline(fit, col = 'blue')
acf(fit$residuals)
pacf(fit$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-15-1.png)<!-- -->

Model output, using standard and Newey-West HAC errors:

``` r
summary(fit) # standard estimates
```

    ## 
    ## Call:
    ## lm(formula = y ~ x)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -2.63213 -0.99396 -0.05379  1.15511  3.00291 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)
    ## (Intercept)  0.71744    0.43512   1.649    0.106
    ## x            0.02203    0.01485   1.483    0.144
    ## 
    ## Residual standard error: 1.515 on 48 degrees of freedom
    ## Multiple R-squared:  0.04384,    Adjusted R-squared:  0.02392 
    ## F-statistic: 2.201 on 1 and 48 DF,  p-value: 0.1445

``` r
coeftest(fit, vcov = NeweyWest(fit, verbose = T))
```

    ## 
    ## Lag truncation parameter chosen: 2

    ## 
    ## t test of coefficients:
    ## 
    ##             Estimate Std. Error t value Pr(>|t|)
    ## (Intercept) 0.717443   0.712958  1.0063   0.3193
    ## x           0.022030   0.033051  0.6665   0.5083

Fit ARIMA model, and plot

``` r
layout.matrix <- matrix(c(1, 2, 1, 3), nrow = 2, ncol = 2)
layout(mat = layout.matrix)

fit_arima <- auto.arima(y, xreg = x)
summary(fit_arima)
```

    ## Series: y 
    ## Regression with ARIMA(1,0,0) errors 
    ## 
    ## Coefficients:
    ##          ar1    xreg
    ##       0.8578  0.0363
    ## s.e.  0.0680  0.0223
    ## 
    ## sigma^2 = 0.6203:  log likelihood = -58.65
    ## AIC=123.31   AICc=123.83   BIC=129.05
    ## 
    ## Training set error measures:
    ##                      ME      RMSE       MAE      MPE     MAPE      MASE
    ## Training set 0.04447121 0.7717022 0.6491208 150.3636 298.8786 0.9782997
    ##                   ACF1
    ## Training set 0.0796193

``` r
plot(x,y)
lines(fit_arima$fitted, col = "blue")
lines(get_slope_line_vector_from_arima(fit_arima), col = "darkgreen")
acf(fit_arima$residuals)
pacf(fit_arima$residuals)
```

![](2022-03-08_newey-west-heteroskedasticity-and-autocorrelation-robust-errors_files/figure-gfm/unnamed-chunk-17-1.png)<!-- -->
