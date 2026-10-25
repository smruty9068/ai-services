import pandas as pd


class main:

    def load_student_enquiry(self):
        df1 = pd.read_csv(
            "C:\\Users\\10880923\\Downloads\\training_enquiries.csv"
        )
        return df1.drop(columns=["enquiry_date"])

    def clean_enquiry_data(self, df1):
        df_mod = df1.dropna(subset=["email"])
        df_mod_uniq = df_mod.drop_duplicates(
            subset=["enquiry_id"],
            keep="first"
        )
        return df_mod_uniq

    def merge_courses(self, df1):
        df2 = pd.read_csv(
            "C:\\Users\\10880923\\Downloads\\training_courses.csv"
        )

        df = pd.merge(
            df1,
            df2,
            on=["course_id"],
            how="inner"
        )
        return df

    def add_net_quoted_fee(self, df):
        df = df.copy()

        df["net_quoted_fee"] = round(
            df["quoted_fee"] * (1 - df["discount_pct"] / 100),
            2
        )

        return df

    def agg_by_coure(self, df):
        res = (
            df.groupby(
                ["course_id", "course_name"],
                as_index=False
            )
            .agg(
                avg_net_quoted_fee=("net_quoted_fee", "mean"),
                Enq_count=("enquiry_id", "count")
            )
        )

        return res

    def fin_summ(self, df):
        df["avg_net_quoted_fee"] = df["avg_net_quoted_fee"].round(2)

        df = df[
            ["course_name", "avg_net_quoted_fee", "Enq_count"]
        ]

        df = (
            df.sort_values(
                by="course_name",
                ascending=True
            )
            .reset_index(drop=True)
        )

        return df


if __name__ == "__main__":

    m = main()

    d1 = m.load_student_enquiry()
    d2 = m.clean_enquiry_data(d1)
    d3 = m.merge_courses(d2)
    d4 = m.add_net_quoted_fee(d3)
    d5 = m.agg_by_coure(d4)
    d6 = m.fin_summ(d5)

    print(d6)