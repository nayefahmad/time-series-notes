Trend-stationary vs difference-stationary time series
================
Nayef Ahmad
2022-07-18

-   [1 Overview](#overview)
-   [2 Libraries](#libraries)
-   [3 Example](#example)

# 1 Overview

# 2 Libraries

``` r
library(forecast)
```

    ## Warning: package 'forecast' was built under R version 4.0.5

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

# 3 Example

``` r
set.seed(2021)

series_length <- 25
ar_coefficient <- .6

y <- arima.sim(series_length, model = list(ar = ar_coefficient))
x <- 1:series_length
plot(x, y)

fit <- lm(y~x)
abline(fit, col = "blue")
```

![](2022-07-18_trend-stationary-versus-difference-stationary-time-series_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->
