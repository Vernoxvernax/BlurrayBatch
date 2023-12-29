# Maintainer: Vernox Vernax <vernoxvernax@gmail.com>

_base=blurrybatch
_lib=BlurryBatch
pkgname=python-${_base}
pkgver=1.0.4
pkgrel=1
pkgdesc="Easy processing of Blu-Rays and DVDs"
license=('MIT')
arch=('any')
url='https://github.com/Vernoxvernax/BlurryBatch'
license=('MIT')
depends=('python')
makedepends=('python-build' 'python-installer')


package(){
  _site="$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
  cp ../BlurryBatch.py .
  install -Dm644 BlurryBatch.py "${pkgdir}${_site}/${_lib}.py"
  python -m compileall -q -f -d "${_site}" "${pkgdir}${_site}/${_lib}.py"
  python -OO -m compileall -q -f -d "${_site}" "${pkgdir}${_site}/${_lib}.py"
}

# vim:set ts=2 sw=2 et:

