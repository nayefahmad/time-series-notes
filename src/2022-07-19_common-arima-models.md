Common ARIMA models
================
Nayef
7/19/2022

-   [1 Overview](#overview)
    -   [1.1 References](#references)
-   [2 Libraries](#libraries)
-   [3 Inspecting `arima.sim()`](#inspecting-arima.sim)

# 1 Overview

## 1.1 References

-   [Robert Nau (Duke University) lecture
    notes](https://people.duke.edu/~rnau/411arim.htm)
-   [Simulating ARIMA models - Free Range Stats blog
    post](http://freerangestats.info/blog/2015/11/21/arima-sims)
-   [Simulating ARIMA models - Sean
    vdM](https://seanvdm.co.za/post/tssim1/)

# 2 Libraries

``` r
library(forecast)
```

    ## Warning: package 'forecast' was built under R version 4.0.5

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

``` r
arima.sim(25, model = list(ar = .5))
```

    ## Time Series:
    ## Start = 1 
    ## End = 25 
    ## Frequency = 1 
    ##  [1]  0.40683357 -1.22908005 -1.87438461  1.30350548  1.11810464  0.96067379
    ##  [7]  1.00530041  2.03447384  2.56340526  1.08052709  0.35527400  0.80316665
    ## [13]  0.23374886  0.66548950 -2.08185896 -1.01520301 -0.12183210 -0.10777718
    ## [19]  1.83703349  0.46507918  0.05577651 -0.28108868  0.60117146 -0.04253630
    ## [25] -1.49738442

``` r
sim_n_reps <- function(reps, n, ar_coeffs){
  replicate(reps, 
            arima.sim(n, model = list(ar = ar_coeffs)))
} 


x <- sim_n_reps(reps = 5, n = 25, ar_coeffs = .5)
x2 <- sim_n_reps(reps = 5, n = 25, ar_coeffs = c(.5, .1))


# Use case: 
# data <- sim_n_reps()
# plot(data)
```

# 3 Inspecting `arima.sim()`

1.  Condition for stationarity of AR model: *ϕ*(*B*) = 0 must have roots
    outside of the unit circle.

``` r
?arima.sim
```

    ## starting httpd help server ... done

``` r
arima_sim2 <- function (model, 
                        n, 
                        rand.gen = rnorm, 
                        innov = rand.gen(n, ...), 
                        n.start = NA, 
                        start.innov = rand.gen(n.start, ...),
                        ...) 
{
  
  if (!is.list(model)) 
    stop("'model' must be list")
  
  if (n <= 0L) 
    stop("'n' must be strictly positive")
  
  
  # p is the order of the AR part of the model
  p <- length(model$ar)
  if (p) {
    minroots <- min(Mod(polyroot(c(1, -model$ar))))
    if (minroots <= 1) 
      # To ensure stationarity, the roots of the polynomial must be 
      #   outside the unit circle. See note 1 above. 
      stop("'ar' part of model is not stationary")
  }
  
  # q is the order of the MA part of the model
  q <- length(model$ma)
  
  # n.start is the length of the burn-in period. If not set by user, 
  # a sensible value is computed: 
  if (is.na(n.start)) 
    n.start <- p + q + ifelse(p > 0,
                              ceiling(6/log(minroots)), 
                              0)
  if (n.start < p + q) 
    stop("burn-in 'n.start' must be as long as 'ar + ma'")
  
  # d is the order of differencing
  d <- 0
  if (!is.null(ord <- model$order)) {
    if (length(ord) != 3L) 
      stop("'model$order' must be of length 3")  # must specify p, d, and q
    if (p != ord[1L]) 
      stop("inconsistent specification of 'ar' order")
    if (q != ord[3L]) 
      stop("inconsistent specification of 'ma' order")
    
    d <- ord[2L]
    if (d != round(d) || d < 0) 
      stop("number of differences must be a positive integer")
  }
  
  
  if (!missing(start.innov) && length(start.innov) < n.start) 
    stop(sprintf(ngettext(n.start, 
                          "'start.innov' is too short: need %d point", 
                          "'start.innov' is too short: need %d points"), 
                 n.start),
         domain = NA)
  
  
  x <- ts(c(start.innov[seq_len(n.start)], innov[1L:n]), start = 1 - 
            n.start)
  
  if (length(model$ma)) {
    x <- filter(x, c(1, model$ma), sides = 1L)
    x[seq_along(model$ma)] <- 0
  }
  
  if (length(model$ar)) 
    x <- filter(x, model$ar, method = "recursive")
  
  if (n.start > 0) 
    x <- x[-(seq_len(n.start))]
  
  if (d > 0) 
    x <- diffinv(x, differences = d)
  
  as.ts(x)
}
```
