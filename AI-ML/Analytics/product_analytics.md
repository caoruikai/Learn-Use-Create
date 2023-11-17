# Learning Notes on Internet Product Analytics
- [Educative Course](https://www.educative.io/courses/ace-the-product-analytics-job-interview)
- YouTube Videos
    - https://youtu.be/jtC3Vs7w2X0
    - https://youtu.be/Afl9uNcJcBI
    - https://youtu.be/nPJKFWMiIC8

# Types of Interview Questions
## Explain Metrics Changes Questions
- Provide potential reasons for changes of metrics.
    - Why was metric X changed?
    - Why did metric X increase but Y decreased?
## Measure Feature Success Questions
- Define proper metrics to measure a product/feature.
    - After launch: How to measure the success of feature X?
    - Before launch: How to decide if feature Y needs to be added/changed?
## Growth Questions
- Focusing on growth:
    - What metrics to use to track the growth?
    - What action to take to grow a metric for a product?

# Answer Flow

## Explain Metrics Changes Questions
1. Ask for contexts
    - Business/Product goals
    - Platform status and trends
    - Target users
    - User flow to use the feature
    - Related products/features
    - Monetization strategy
2. Ask for the metrics
    - Definition
    - Formula. Fractional?
3. Ask for the changes of metrics
    - Long term trend or one-time event?
    - Seasonality? Speical dates like weekends or holidays?
    - Special events? Natural disaster? Launch of other products?
4. Draw hypothesis
    - If 2 metrics were asked
        - Find the relation between 2 metrics
        - If not given, find the action/event behind that may change both metrics
        - Segment by "action metrics", and measure the other 2 metrics
        - Prioritze the 2 metrics: which one is more important for the product goal? Or are both bad metrics?
    - Segment users
        - By Demographics
            - Locations
            - Ages
        - By Tenure
            - New v.s. Existing
            - Split by tenure cohort
        - By Engagement
            - DAU/WAU/MAU
            - Time Spent
        - By User Flow
            - Acquisition channels
            - Device / Platform
    - Segment activities
        - By User Flow / Access Point
            - Recommendation
            - Friends / Connections
            - Groups
            - Search
            - Direct communications: email, text
        - By Activity Types
            - Post types
            - Notification types
5. Propose Data Analysis to prove or disprove the hypothesis
    - Measure the metrics of interest
        - for each segmentation
        - across time
        - compare with other similar samples (other location, time period, etc.)

## Measure Feature Success Questions
1. Ask for contexts
    - Business/Product goals
    - Platform status and trends
    - Target users
    - User flow to use the feature
    - Related products/features
    - Monetization strategy
2. Discuss user Flow / Funnel
    1. Acquisition (onboard the product)
    2. Conversion (purchase, daily active)
    3. Engagement (active)
    4. Retention (short and long term)
3. Find "Goal Metrics"
    1. Determine the primary goal
        - Acquisition? (Growth)
        - Conversion?
        - Engagement?
        - Retention? (Long-term)
        - Revenue?
    2. Find a metric that reflects the goal
        - Acquisition: new user acquisition per day
        - Conversion: number of purchases per day
        - Engagement: number of activities per day
        - Retention: length of usage over a year
        - Revenue: purchase amount
4. After Launch Questions v.s Before Launch Questions
    - If the feature was launched/updated
        1. Find "Feature Metrics"
            - Represent the health of the feature/product
            - Metrics needs to monitor daily
        2. Analysis: Connect "feature Metrics" with "Goal Metrics"
            1. Group by "feature metric", calculate the average "goal metric"
            2. Examine the correlation between the "goal metric" and the buckets of "feature metric"
            3. Design a composed metric like: average of "goal metric" grouped by "feature metric"
    - If the feature was not launched/updated
        1. Find "feature metrics" that will be changed once the feature is launched
        2. Optionally, do A/B test. Then "after launch" data is available.
        3. Analysis: predict effects of feature launch/update
            1. Segment the data using "feature metrics"
            2. Observe the data patterns
                - How large is each bucket? (room of improvement)
                - What are the trends of "goal metric" when "feature metrics" change?
        4. Conclude the effect and make a launch decision

## Growth Questions
- Hyposthesize on effects that attracts people
- Design metrics reflecting that effects
    - Metrics must be measurable from existing data or can be obtained in A/B tests
- Conduct A/B test, using segments of metrics
- Alternatively, using existing data in analysis