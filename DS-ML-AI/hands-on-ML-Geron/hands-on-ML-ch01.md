# Chapter 1 - The Fundamentals of Machine Learning
## Summary
- **What is Machine Learning?**
    - "A computer program is said to learn from experience E with respect to some task T and some performance measure P, if its performance on T, as measured by P, improves with experience E." - Tom Mitchell, 1997
- **Why Use Machine Learning?**
    - Machine Learning is great for:
        1. Problems for which existing solutions require a lot of hand-tuning or long lists of rules: one Machine Learning algorithm can often simplify code and perform better, especially when the rules might be changed (e.g. email spam filter).
        2. Complex problems for which there is no good solution at all using a traditional approach: the best Machine Learning techniques can perhaps find a solution, and often are more scalable (e.g. voice recognition).
        3. Fluctuating environments: a Machine Learning system can adapt to new data.
        4. Getting insights about complex problems and large amounts of data (data mining).     
- **Types of Machine Learning Systems**
    - It is useful to classify Machine Learning systems in broad categories based on:
        1. Whether or not they are trained with human supervision (supervised, unsupervised, semisupervised, and Reinforcement Learning)
        2. Whether or not they can learn incrementally on the fly (online versus batch learning)
        3. Whether they work by simply comparing new data points to known data points, or instead detect patterns in the training data and build a predictive model, much like scientists do (instance-based versus model-based learning)
- **Main Challenges of Machine Learning**
    - **Bad Data**
        - Insufficient Quantity of Training Data
        - Nonrepresentative Training Data
        - Poor-Quality Data
        - Irrelevant Features
    - **Bad Algorithm**
        - Overfitting the Training Data
        - Underfitting the Training Data
- **Testing and Validating**
    - To evaludate the performance of the model, split the data set into **training set** and **test set**: train the model using the training set while evaluate the performance in the test set.
    - **Hyperparameter Tuning and Model Selection**
        - **Holdout Validation**: you simply hold out part of the training set to evaluate several candidate models and select the best one. The new heldout set is called the **validation set** (or sometimes the **development set**, or **dev set**). More specifically, you train multiple models with various hyperparameters on the reduced training set (i.e., the full training set minus the validation set), and you select the model that performs best on the validation set. After this holdout validation process, you train the best model on the full training set (including the validation set), and this gives you the final model. Lastly, you evaluate this final model on the test set to get an estimate of the generalization error.
    - **Data Mismatch**
        - `S` is a mixed sample from both population `A` and population `B`. The model will eventually be tested on a sample from population `B`. Now randomly split the sample from `B` into two halves. The first half is used as  validation set, the other half is used as test set. The sample from `A` is used as the training set. But if the model performs poorly on the validation or test set, it is difficult to tell whether it is due to the model itself or data mismatch between training and validation (or test) sets. One way to solve it is to randomly sample the training set to get **train-dev** set. Now if the model performs well on train-dev set but not validation set, we know it is because the data mismatch.
- **No Free Lunch Theorem**: if you make absolutely no assumption about the data, then there is no reason to prefer one model over any other.

## Exercises

1. How would you define Machine Learning?
    - A: Quote from Tom Mitchell (see above)
2. Can you name four types of problem where it shines?
    - A: See summary above   
3. What is a labeled training set?
    - A: Labeled training set is a data set where the true values of the target variable is known (labeled).
4. What are the two most common supervised tasks?
    - A: Classification and Regression
5. Can you name four common unsupervised tasks?
    - A: Clustering, Anomaly Detection & Novelty Detection, Visualization & Dimensionality Reduction, Association Rule Learning
6. What type of Machine Learning algorithm would you use to allow a robot to walk in various unknown terrains?
    - A: Reinforcement Learning
7. What type of algorithm would you use to segment your customers into multiple groups?
    - A: Clustering
8. Would you frame the problem of spam detection as a supervised learning problems or an unsupervised learning problem?
    - A: Supervised learning
9. What is an online learning system?
    - A: In online learnig, you train the system incrementally by feeding it data instances sequentially, either individually or by small groups called mini-batches.       
10. What is out-of-core learning?
    - A: Systems trained on huge datasets that cannot fit in one machine's main memory.        
11. What type of learning algorithms relies on a similarity measure to make predictions?
    - A: Instance-based learning      
12. What is the difference between a model parameter and a learning algorithm's hyperparameter?
    - A: A hyperparameter is a parameter of a learning algorithm, not of the model. It is not affected by the learning algorithm itself; it must be set prior to training and remains constant during training.        
13. What do model-based learning algorithms search for? What is the most common strategy they use to succeed? How do they make predictions?
    - A: Model-based learning algorithms search for the model parameter values that minimize a cost function.      
14. Can you name four of the main challenges in Machine Learning?
    - A: See summary above        
15. If your model performs great on the training data but generalize poorly to the new instances, what is happening? Can you name three possible solutions?
    - A: Overfitting happens. Possible solutions: 1. Simplify models by selecting the ones with fewer paramters or by reducing number of attributes or by constraining the model; 2. Gether more training data; 3. To reduce the noice in the training data (fix data errors and remove outliers).        
16. What is a test set and why would you want to use it?
    - A: Test set is the subset of data used to test the performance of the model. We use test set because the only way to know how well a model generalize to new cases is to actually try it out on new cases.    
17. What is the purpose of a validation set?
    - A: To choose the best model (e.g. hyperparameter tuning).    
18. What is the train-dev set, when do you need it and how do you use it?
    - A: See summary        
19. What can go wrong if you tune hyperparameters using the test set?
    - A: When the model is delployed, the performance on the new data set might be worse than on the test set. The problem is that you measured the generalization error multiple times on the test set, and you adapted your model and hyperparameters to produce the best model for that particular set.