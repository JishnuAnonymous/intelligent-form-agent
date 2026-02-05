import os
import subprocess
import sys

def run_command(cmd):
    print(f"\n[RUNNING] {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Intelligent Form Agent Demo ===")
    
    # 1. Generate Data
    if not os.path.exists('data/samples'):
        print("Generating test data...")
        import demo_data_gen
        demo_data_gen.generate_samples()

    # 2. Process Folder (Ingestion)
    print("\n--- Step 1: Ingesting Forms from Folder ---")
    run_command(f"{sys.executable} -m src.main --folder data/samples")
    
    # 3. Ask Question (Single Form)
    print("\n--- Step 2: QA on Single Form (Form 1) ---")
    # We assume form_id 1 corresponds to the first processed file.
    # In a real scenario we'd query IDs, but reset DB or assume empty starts
    run_command(f'{sys.executable} -m src.main --ask "What is the invoice number?" --form_id 1')
    
    # 4. Summary (Single Form)
    print("\n--- Step 3: Summary of a Form (Form 3) ---")
    run_command(f"{sys.executable} -m src.main --summary --form_id 3")

    # 5. Holistic QA
    print("\n--- Step 4: Holistic QA (Ask All) ---")
    run_command(f'{sys.executable} -m src.main --ask "Who are the customers?" --ask_all')

if __name__ == "__main__":
    main()
