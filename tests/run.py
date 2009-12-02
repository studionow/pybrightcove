import sys, os

os.chdir(os.path.dirname(__file__))

try:
    import nose
except ImportError:
    print ('nose is required to run the Pygments test suite')
    sys.exit(1)

try:
    # make sure the current source is first on sys.path
    sys.path.insert(0, '..')
    import sn
except ImportError:
    print ('Cannot find sn to test: %s' % sys.exc_info()[1])
    sys.exit(1)

nose.main()
