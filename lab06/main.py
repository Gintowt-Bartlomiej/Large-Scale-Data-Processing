import os
import random
import string
from pyspark.sql.functions import length, sum as spark_sum
from pyspark.sql import SparkSession
import time


def get_session(app_name: str) -> SparkSession:
    spark_master_url = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
    return (
        SparkSession.builder
        .appName(app_name)
        .master(spark_master_url)
        .getOrCreate()
    )


def example() -> None:
    spark = get_session("Example app")

    df = spark.createDataFrame(
        data=[
            (1, "Alice"),
            (2, "Bob"),
            (3, "Charlie"),
        ],
        schema=["id", "name"],
    )

    df.show()

    print(f"Total rows: {df.count()}")

    spark.stop()


def generate_numbers():
    spark = get_session("Number generator app")

    sc = spark.sparkContext
    seeds = list(range(10))

    rdd = sc.parallelize(seeds, numSlices=10)

    def generate_random_numbers(seed: int):
        rng = random.Random(seed)
        count = 1_000_000
        return [rng.random() for _ in range(count)]

    numbers_rdd = rdd.flatMap(generate_random_numbers)
    total_count = numbers_rdd.count()
    print(f"\nGenerated {total_count} numbers.")
    
    numbers_df = numbers_rdd.map(lambda x: (x,)).toDF(["value"])
    print("5 examples:")
    numbers_df.show(5)

    spark.stop()



def create_random_strings(output_path: str = "/wyniki/random_strings", min_len: int = 5, max_len: int = 20):
    spark = get_session("Create random strings app")
    sc = spark.sparkContext

    count = 1_000_000
    partitions = 10

    base_rdd = sc.parallelize(range(count), partitions)

    def generate_random_string(_: int) -> str:
        length = random.randint(min_len, max_len)
        letters = string.ascii_letters
        return ''.join(random.choices(letters, k=length))

    strings_rdd = base_rdd.map(generate_random_string)

    strings_df = strings_rdd.map(lambda s: (s,)).toDF(["value"])

    print(f"\nAttempting to save {count} strings to: {output_path}")
    strings_df.write.mode("overwrite").text(output_path)

    print(f"Successfully saved strings to: {output_path}")

    spark.stop()


def count_characters(input_path: str = "/wyniki/random_strings"):
    spark = get_session("Count characters app")

    strings_df = spark.read.text(input_path)

    print(f"\nNumber of loaded string: {strings_df.count()}")

    total_chars = strings_df.select(spark_sum(length("value"))).first()[0]

    print(f"All characters count: {int(total_chars)}")

    print("5 examples:")
    strings_df.show(5, truncate=False)

    # Sleep
    print("Sleeping")
    time.sleep(600)

    spark.stop()


def main():
    example()

    generate_numbers()

    create_random_strings()

    count_characters()


if __name__ == "__main__":
    main()
    