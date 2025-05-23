{
  "variables": {
    "module_name%": "node_printer",
    "module_path%": "lib",
    "openssl_fips": ""
  },
  'targets': [
    {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": [ "<(module_name)" ],
      "copies": [
        {
          "files": [ "<(PRODUCT_DIR)/<(module_name).node" ],
          "destination": "<(module_path)"
        }
      ]
    },
    {
      'target_name': 'node_printer',
      'sources': [
        # is like "ls -1 src/*.cc", but gyp does not support direct patterns on
        # sources
        '<!@(["python", "tools/getSourceFiles.py", "src", "cc"])'
      ],
      'include_dirs' : [
        "<!(node -e \"require('nan')\")"
      ],
      'cflags_cc': [
        "-DNOMINMAX",
        "-Wno-deprecated-declarations"
      ],
      'conditions': [
        # common exclusions
        ['OS!="linux"', {'sources/': [['exclude', '_linux\\.cc$']]}],
        ['OS!="mac"', {'sources/': [['exclude', '_mac\\.cc|mm?$']]}],
        ['OS!="win"', {
          'sources/': [['exclude', '_win\\.cc$']]}, {
          # else if OS==win, exclude also posix files
          'sources/': [['exclude', '_posix\\.cc$']],
          'defines': [
            'NOMINMAX'
          ]
        }],
        # specific settings
        ['OS!="win"', {
          'cflags':[
            '<!(cups-config --cflags)'
          ],
          'ldflags':[
            '<!(cups-config --libs)'
            #'-lcups -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err -lz -lpthread -lm -lcrypt -lz'
          ],
          'libraries':[
            '<!(cups-config --libs)'
            #'-lcups -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err -lz -lpthread -lm -lcrypt -lz'
          ],
          'link_settings': {
            'libraries': [
              '<!(cups-config --libs)'
            ]
          }
        }],
        ['OS=="mac"', {
          'cflags':[
            "-stdlib=libc++"
          ],
          'xcode_settings': {
            "OTHER_CPLUSPLUSFLAGS":["-std=c++20", "-stdlib=libc++"],
            "OTHER_LDFLAGS": ["-stdlib=libc++"],
            "MACOSX_DEPLOYMENT_TARGET": "10.14",
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "CLANG_CXX_LIBRARY": "libc++",
            "CLANG_CXX_LANGUAGE_STANDARD": "c++20"
          },
        }],
      ]
    }
  ]
}
