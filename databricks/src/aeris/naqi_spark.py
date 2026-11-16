"""NAQI in Spark: join each daily value to its breakpoint band (broadcast join, no UDF)."""

from pyspark.sql.functions import broadcast, col, least, lit, round as round_, when

from aeris.breakpoints import BREAKPOINTS, CATEGORY_BANDS


def breakpoints_df(spark):
    rows, prev_hi = [], {}
    for p, lo, hi, i_lo, i_hi, cat in BREAKPOINTS:
        rows.append((p, float(prev_hi.get(p, -1)), float(lo), float(hi), float(i_lo), float(i_hi)))
        prev_hi[p] = hi
    last_hi = {p: hi for p, _, _, hi, _, _ in rows}
    rows = [r + (r[3] == last_hi[r[0]],) for r in rows]
    return spark.createDataFrame(rows, "pollutant string, prev_hi double, bp_lo double, bp_hi double, "
                                       "i_lo double, i_hi double, is_last boolean")


def add_sub_index(df, spark, value_col="daily_value"):
    bp = breakpoints_df(spark)
    v = col(value_col)
    in_band = (df.pollutant == bp.pollutant) & (v > bp.prev_hi) & ((v <= bp.bp_hi) | bp.is_last)
    return (df.join(broadcast(bp), in_band, "inner").drop(bp.pollutant)
              .withColumn("sub_index", least(round_((col("i_hi") - col("i_lo")) / (col("bp_hi") - col("bp_lo"))
                                                    * (v - col("bp_lo")) + col("i_lo")), lit(500)).cast("int"))
              .drop("prev_hi", "bp_lo", "bp_hi", "i_lo", "i_hi", "is_last"))


def category(c):
    expr = None
    for top, name in CATEGORY_BANDS:
        expr = when(c <= top, name) if expr is None else expr.when(c <= top, name)
    return expr
