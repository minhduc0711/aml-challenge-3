import pandas as pd


def create_submission(test_df, preds):
    target_conversion = {
        0: 0,
        1: 1,
        2: -1
    }
    submission_df = pd.DataFrame({"textID": test_df["textID"], "sentiment": preds})
    submission_df["sentiment"] = submission_df['sentiment'].map(target_conversion)
    submission_df.to_csv("submission.csv", index=False)