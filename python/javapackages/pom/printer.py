class Printer(object):
    @staticmethod
    def get_mvn_str(gid, aid, ext="", cla="", ver=""):
        mvnstr = "{gid}:{aid}".format(gid=gid, aid=aid)

        if ext:
            mvnstr = mvnstr + ":{ext}".format(ext=ext)

        if cla:
            if not ext:
                mvnstr = mvnstr + ":"
            mvnstr = mvnstr + ":{cla}".format(cla=cla)

        if ver:
            mvnstr = mvnstr + ":{ver}".format(ver=ver)
        elif cla or ext:
            mvnstr = mvnstr + ":"

        return mvnstr

    @staticmethod
    def get_rpm_str(gid, aid, ext="", cla="", ver="", namespace="",
                    compat=False, pkgver=None):

        mvnstr = Printer.get_mvn_str(gid, aid, ext, cla, ver if compat else "")
        rpmstr = "mvn({mvnstr})".format(mvnstr=mvnstr)

        if namespace:
            rpmstr = "{ns}-{rpmstr}".format(ns=namespace, rpmstr=rpmstr)

        if pkgver is not None:
            rpmstr = "{rpmstr} = {ver}".format(rpmstr=rpmstr, ver=pkgver)

        return rpmstr
