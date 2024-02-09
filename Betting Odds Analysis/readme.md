# Betting Odds Analysis
Project cointaing:
- data collection - Betting odds data are collected from today's and tomorrow's matches. The collected data is stored in CSV format. CSV files are merged and supplemented to create comprehensive datasets.
- data analysis - Extensive analysis is conducted on the collected data to derive insights.
- neural network - NN are under development due to lack of data. One of many possible approaches is presented, the effects of NN need to be improved

## Results of data analysis.
Simulations have been prepared. Each time simulation starts with 100 money on account, 1000 tests, 40 bets in each test.


1 match in bet:
| Winrate (%) | Percentage | Average Money | Bankruptcy | Losses | First Quartile | Second Quartile | Third Quartile |
|:------------|------------|---------------|------------|--------|----------------|-----------------|----------------|
| 70.31       | 0.02       | 106.13        | 0          | 348    | 98.59          | 104.99          | 112.67         |
| 70.31       | 0.05       | 119.04        | 0          | 257    | 99.53          | 116.2           | 135.04         |
| 70.31       | 0.08       | 133.67        | 0          | 274    | 97.56          | 124.71          | 160.97         |
| 70.31       | 0.12       | 155.77        | 0          | 302    | 92.19          | 133.62          | 198.26         |
| 70.31       | 0.15       | 174.75        | 0          | 325    | 85.18          | 137.73          | 226.35         |
| 70.31       | 0.20       | 210.99        | 0          | 375    | 70.62          | 135.78          | 268.34         |

2 match in bet:
| Winrate (%) | Percentage | Average Money | Bankruptcy | Losses | First Quartile | Second Quartile | Third Quartile |
|:------------|------------|---------------|------------|--------|----------------|-----------------|----------------|
| 49.07       | 0.02       | 125.51        | 0          | 131    | 111.08         | 126.19          | 138.51         |
| 49.07       | 0.05       | 193.92        | 0          | 93     | 133.36         | 178.43          | 236.71         |
| 49.07       | 0.08       | 300.52        | 0          | 117    | 149.73         | 242.09          | 378.23         |
| 49.07       | 0.12       | 538.56        | 0          | 149    | 152.01         | 325.69          | 638.19         |
| 49.07       | 0.15       | 837.74        | 0          | 170    | 149.65         | 374.99          | 874.77         |
| 49.07       | 0.20       | 1805.25       | 0          | 220    | 119.2          | 417.87          | 1272.15        |

3match in bet:
| Winrate (%) | Percentage | Average Money | Bankruptcy | Losses | First Quartile | Second Quartile | Third Quartile |
|:------------|------------|---------------|------------|--------|----------------|-----------------|----------------|
| 34.41       | 0.02       | 153.4         | 0          | 59     | 127.35         | 147.55          | 175.59         |
| 34.41       | 0.05       | 351.11        | 0          | 46     | 178.28         | 280.5           | 429.67         |
| 34.41       | 0.08       | 772.27        | 0          | 76     | 217.41         | 437.05          | 868.53         |
| 34.41       | 0.12       | 2110.95       | 0          | 96     | 232.06         | 645.89          | 1722.02        |
| 34.41       | 0.15       | 4279.34       | 1          | 120    | 216.63         | 749.08          | 2437.26        |
| 34.41       | 0.20       | 12754.83      | 4          | 197    | 157.17         | 760.91          | 3498.22        |

## Data visualization
In the data visualization file, we can draw a chart for selected leagues and types of bets. Charts can be saved for comparison. It is possible to display a list of matches that ended in failure (you can analyze which clubs do not provide predictable results).

The chart shows the value of the expected profit (without tax) for the plant in the given range. The graph can also be smoothed - we take into account neighboring values, which reduces noise
![image](https://github.com/kiper22/portfolio/assets/125763668/f8f39a07-45ad-488e-ad6c-30578ee0b2e4)

## Neural Networks
NN are under development. Lately i found web page with huge amount of match data which can be used to learning. Currently, a version for a very simple NN has been prepared.
