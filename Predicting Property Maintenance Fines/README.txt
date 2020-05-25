This assignment was to create a supervised learning algorithm that would predict whether a given property maintenance
ticket (specifically in the state of Michigan) would be paid on time.  Using only a provided set of past ticket
information as training data for the model, the task scope included:

--Cleaning the data (joining multiple files, fixing typos, etc.)
--Feature selection and quantification
--Model selection and testing

The resulting model's predictions for the test data were scored by ROC AUC, with 0.7 being the minimum score required to
 pass the assignment.

The random forest classifier from sklearn proved to be effective at making predictions for the test data, and was the
specific learning algorithm trained and submitted for the task.