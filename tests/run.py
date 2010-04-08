import sys, os

os.chdir(os.path.dirname(__file__))

try:
    import nose
except ImportError:
    print ('nose is required to run the Pygments test suite')
    sys.exit(1)

nose.main()
