from PyQt5.QtCore import QT_TR_NOOP


version = "0.0.1"

about = QT_TR_NOOP("""<h1>bqup</h1>

<p>A Qt frontend to <a href="">bup</a> backup system</p>

<p>Version {version}</p>

<p>Writen by Charles Brunet</p>
""").format(version=version)
