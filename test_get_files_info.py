from functions.get_files_info import get_files_info

def main():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("\nResult for /bin:")
    print(result)

    result = get_files_info("calculator", "../")
    print("\nResult for ../:")
    print(result)

    result = get_files_info("calculator", "main.py")
    print("\nResult for main.py:")
    print(result)

if __name__ == "__main__":
    main()