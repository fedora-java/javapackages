import logging

# Silence PyXB "Unable to convert DOM node" warnings
logging.getLogger("pyxb.binding.basis").setLevel(logging.ERROR)
