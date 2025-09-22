import random
import string
import sys
import argparse
from pyflink.common import Types, Encoder, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.file_system import FileSink, OutputFileConfig, RollingPolicy, StreamFormat, FileSource
import re


def generate_random_doubles(output_path, count=100000):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    env.set_parallelism(1)

    # Generate random doubles
    data = (random.uniform(0, 1000) for _ in range(count))
    ds = env.from_collection(data, type_info=Types.DOUBLE())

    sink = FileSink.for_row_format(
        output_path,
        Encoder.simple_string_encoder()
    ).with_output_file_config(
        OutputFileConfig.builder().with_part_prefix("doubles").with_part_suffix(".txt").build()
    ).with_rolling_policy(RollingPolicy.default_rolling_policy()).build()

    ds.sink_to(sink)
    env.execute("Generate Random Doubles")


def generate_random_strings(output_path, count=10000, min_len=5, max_len=15):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    env.set_parallelism(1)

    def random_string():
        length = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    data = (random_string() for _ in range(count))
    ds = env.from_collection(data, type_info=Types.STRING())

    sink = FileSink.for_row_format(
        output_path,
        Encoder.simple_string_encoder()
    ).with_output_file_config(
        OutputFileConfig.builder().with_part_prefix("strings").with_part_suffix(".txt").build()
    ).with_rolling_policy(RollingPolicy.default_rolling_policy()).build()

    ds.sink_to(sink)
    env.execute("Generate Random Strings")


def count_total_characters(input_path, output_path=None):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    env.set_parallelism(4)
    
    ds = env.from_source(
        source=FileSource.for_record_stream_format(
            StreamFormat.text_line_format(),
            input_path
        ).process_static_file_set().build(),
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name="file_source"
    )
    
    char_counts = ds.map(lambda s: len(s), output_type=Types.INT())
    
    total_chars = char_counts.map(lambda count: ('total', count), output_type=Types.TUPLE([Types.STRING(), Types.INT()])) \
        .key_by(lambda pair: pair[0]) \
        .reduce(lambda a, b: (a[0], a[1] + b[1]))
    
    result_ds = total_chars.map(
        lambda pair: f"Total number of characters: {pair[1]}", 
        output_type=Types.STRING()
    )
    
    result_ds.sink_to(
        sink=FileSink.for_row_format(
            base_path=output_path,
            encoder=Encoder.simple_string_encoder()
        )
        .with_output_file_config(
            OutputFileConfig.builder()
            .with_part_prefix("character_count_")
            .with_part_suffix(".txt")
            .build()
        )
        .with_rolling_policy(RollingPolicy.default_rolling_policy())
        .build()
    )
    
    env.execute("Count Characters in Random Strings")

def count_words(input_path, output_path):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    
    ds = env.from_source(
        source=FileSource.for_record_stream_format(
            StreamFormat.text_line_format(),
            input_path
        ).process_static_file_set().build(),
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name="file_source"
    )
    
    def split(line):
        line = re.sub(r'[^\w\s]', '', line.lower())
        yield from line.split()
    
    word_counts = ds.flat_map(split) \
        .filter(lambda word: word != '') \
        .map(lambda word: (word, 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()])) \
        .key_by(lambda pair: pair[0]) \
        .reduce(lambda a, b: (a[0], a[1] + b[1]))
    
    collected_results = word_counts.execute_and_collect()
    sorted_results = sorted(collected_results, key=lambda x: x[1], reverse=True)
    
    sorted_counts = env.from_collection(
        sorted_results, 
        type_info=Types.TUPLE([Types.STRING(), Types.INT()]))
    
    formatted_counts = sorted_counts.map(
        lambda pair: f"{pair[0]}: {pair[1]}", 
        output_type=Types.STRING()
    )
    
    formatted_counts.sink_to(
        sink=FileSink.for_row_format(
            base_path=output_path,
            encoder=Encoder.simple_string_encoder()
        )
        .with_output_file_config(
            OutputFileConfig.builder()
            .with_part_prefix("word_count_")
            .with_part_suffix(".txt")
            .build()
        )
        .with_rolling_policy(RollingPolicy.default_rolling_policy())
        .build()
    )
    
    env.execute("Count Words in Wikipedia Article")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', required=True, choices=['doubles', 'strings', 'count', 'wiki'], help='Which task to run')

    args = parser.parse_args()

    if args.task == 'doubles':
        generate_random_doubles(output_path="/opt/flink/data/output/doubles", count=100000)

    elif args.task == 'strings':
        generate_random_strings(output_path="/opt/flink/data/output/strings", count=10000, min_len=5, max_len=20)

    elif args.task == 'count':
        count_total_characters(input_path="/opt/flink/data/output/strings", output_path="/opt/flink/data/output/char_count")

    elif args.task == 'wiki':
        count_total_characters(input_path="/opt/flink/data/input", output_path="/opt/flink/data/output/words_count")
