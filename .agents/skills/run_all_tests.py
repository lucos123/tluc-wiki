"""
Unified Test Runner — Discovers and executes all skill script unit test suites.

Usage:
    python .agents/skills/run_all_tests.py
"""

import os
import sys
import unittest


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    skills_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"=== Discovering Skill Script Unit Tests in {skills_dir} ===\n")

    loader = unittest.TestLoader()
    master_suite = unittest.TestSuite()

    for root, _dirs, files in os.walk(skills_dir):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                file_path = os.path.join(root, f)
                dir_path = os.path.dirname(file_path)
                module_name = f[:-3]

                if dir_path not in sys.path:
                    sys.path.insert(0, dir_path)

                try:
                    suite = loader.loadTestsFromName(module_name)
                    master_suite.addTest(suite)
                except Exception as e:
                    print(f"Error loading {module_name} from {dir_path}: {e}")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(master_suite)

    if result.wasSuccessful():
        print(f"\n✅ ALL {result.testsRun} SKILL SCRIPT UNIT TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"\n❌ UNIT TESTS FAILED: {len(result.failures)} Failures, {len(result.errors)} Errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
