# Iteration 4 — BERTScore paired perturbation

- model: roberta-large, device: cuda
- total pairs: 1630

### Overall (all languages)
- n=1630
- mean=-0.0004 median=+0.0002 stdev=0.0092
- mean|x|=0.0067
- exact_zero=0/1630  near_zero(|x|<0.01)=1269/1630
- sign: syn>ant: 831/1630   syn<ant: 799/1630

## Per language

### cpp
- n=162
- mean=-0.0007 median=+0.0003 stdev=0.0099
- mean|x|=0.0070
- exact_zero=0/162  near_zero(|x|<0.01)=123/162
- sign: syn>ant: 82/162   syn<ant: 80/162

### cs
- n=201
- mean=-0.0021 median=-0.0019 stdev=0.0099
- mean|x|=0.0075
- exact_zero=0/201  near_zero(|x|<0.01)=154/201
- sign: syn>ant: 84/201   syn<ant: 117/201

### go
- n=217
- mean=-0.0006 median=+0.0011 stdev=0.0076
- mean|x|=0.0052
- exact_zero=0/217  near_zero(|x|<0.01)=184/217
- sign: syn>ant: 123/217   syn<ant: 94/217

### java
- n=190
- mean=+0.0010 median=+0.0014 stdev=0.0088
- mean|x|=0.0066
- exact_zero=0/190  near_zero(|x|<0.01)=154/190
- sign: syn>ant: 106/190   syn<ant: 84/190

### js
- n=211
- mean=-0.0011 median=+0.0002 stdev=0.0102
- mean|x|=0.0075
- exact_zero=0/211  near_zero(|x|<0.01)=161/211
- sign: syn>ant: 108/211   syn<ant: 103/211

### php
- n=224
- mean=+0.0016 median=+0.0014 stdev=0.0095
- mean|x|=0.0072
- exact_zero=0/224  near_zero(|x|<0.01)=166/224
- sign: syn>ant: 132/224   syn<ant: 92/224

### py
- n=207
- mean=-0.0007 median=-0.0009 stdev=0.0085
- mean|x|=0.0065
- exact_zero=0/207  near_zero(|x|<0.01)=156/207
- sign: syn>ant: 91/207   syn<ant: 116/207

### rust
- n=218
- mean=-0.0008 median=-0.0004 stdev=0.0087
- mean|x|=0.0063
- exact_zero=0/218  near_zero(|x|<0.01)=171/218
- sign: syn>ant: 105/218   syn<ant: 113/218

