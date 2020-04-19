# HeaderNotice

Python script to insert a custom header notice to C++/C source files (replacing existing ones, if applicable)

Usage:
```shell
python InsertCustomHeaderNotice.py my_source_dir
```

This will recursively replace the header notice in all .cpp, .hpp, .c and .h files in `my_source_dir` and its subdirectories.

To customize the actual header notice, edit the `custom_header` variable in the python script.

