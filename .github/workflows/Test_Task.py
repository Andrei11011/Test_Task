import argparse
import filecmp
import os
import shutil
import logging
import time

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def sync_folders(source_dir, replica_dir):
    try:
        dcmp = filecmp.dircmp(source_dir, replica_dir)

        for sub_dir in dcmp.common_dirs:
            sync_folders(os.path.join(source_dir, sub_dir), os.path.join(replica_dir, sub_dir))

        for file in dcmp.left_only:
            src_file = os.path.join(source_dir, file)
            dest_file = os.path.join(replica_dir, file)
            shutil.copy2(src_file, dest_file)
            logging.info(f"File copied: {src_file} -> {dest_file}")

        for file in dcmp.right_only:
            dest_file = os.path.join(replica_dir, file)
            os.remove(dest_file)
            logging.info(f"File removed: {dest_file}")

    except Exception as e:
        logging.error(f"Error during synchronization: {e}")

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Log file path")

    args = parser.parse_args()
    source_dir = args.source
    replica_dir = args.replica
    interval = args.interval
    log_file = args.log_file

    setup_logging(log_file)

    while True:
        logging.info("Starting synchronization...")
        sync_folders(source_dir, replica_dir)
        logging.info("Synchronization complete.")
        time.sleep(interval)

if __name__ == "__main__":
    main()
