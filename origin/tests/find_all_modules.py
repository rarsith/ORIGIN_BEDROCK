import os
import modulefinder


def find_imports(start_script):
    finder = modulefinder.ModuleFinder()

    # Analyze the starting script
    finder.run_script(start_script)

    # Get all the used modules
    all_modules = set(finder.modules.keys())

    # Optionally, filter out built-in Python modules
    # external_modules = {name for name in all_modules if not name.startswith('_')}

    return all_modules


if __name__ == '__main__':
    repo_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK"
    main_script = os.path.join(repo_path, 'master.py')

    modules = find_imports(main_script)
    print("Used Modules:")
    for module in sorted(modules):
        print(module)
