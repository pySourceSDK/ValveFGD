from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()


def FgdWrite(fgd, filename, collapse=False):

    fgd_text = fgd.fgd_str(collapse=collapse)

    f = open(filename, "w")
    f.write(fgd_text)
    f.close()
