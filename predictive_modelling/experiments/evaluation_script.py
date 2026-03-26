from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


def _positive_class_scores(model, X_test):
    # Prefer decision scores for margin-based models such as SVM.
    if hasattr(model, "decision_function"):
        return model.decision_function(X_test)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)
        classes = getattr(model, "classes_", None)

        if classes is not None:
            for positive_label in (True, 1, "True", "1"):
                if positive_label in classes:
                    positive_index = list(classes).index(positive_label)
                    return probabilities[:, positive_index]

        return probabilities[:, -1]

    raise AttributeError("Model must implement decision_function or predict_proba for ROC-AUC.")


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_score = _positive_class_scores(model, X_test)

    return {
        "Recall_Churn": recall_score(y_test, y_pred),
        "Precision_Churn": precision_score(y_test, y_pred),
        "F1_Churn": f1_score(y_test, y_pred),
        "ROC_AUC": roc_auc_score(y_test, y_score),
    }

