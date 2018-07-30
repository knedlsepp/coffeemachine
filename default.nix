{ nixpkgs ? (builtins.fetchGit {
    url = git://github.com/NixOS/nixpkgs-channels;
    ref = "nixos-18.03";
    rev = "08d245eb31a3de0ad73719372190ce84c1bf3aee";
  })
, getPythonVersion ? (p: p.python2Packages)
, src ? builtins.fetchGit ./.
}:
let
  overlays = [ ];
  pkgs = import nixpkgs { inherit overlays; config = { }; };
  pyPkgs = getPythonVersion pkgs;
  pyDes = pyPkgs.buildPythonPackage rec {
    pname = "pyDes";
    version = "2.0.1";
    src = pyPkgs.fetchPypi {
      inherit pname version;
      sha256 = "04lh71f47y04vspfrdrq6a0hn060ibxvdp5z1pcr0gmqs8hqxaz2";
    };
  };
  ndeflib = pyPkgs.buildPythonPackage rec {
    pname = "ndeflib";
    version = "0.3.2";
    src = pyPkgs.fetchPypi {
      inherit pname version;
      sha256 = "0npn6lw9nj63rn35gfkzqila56dld8zypxa4shkbqa1aw8rqg7aa";
    };
  };
  nfcpy = pyPkgs.buildPythonPackage rec {
    pname = "nfcpy";
    version = "0.13.5";
    src = pyPkgs.fetchPypi {
      inherit pname version;
      sha256 = "1cipgw1gg9abmhq51ix78b7gxk1rphlh2wj4pxr8200vgk4l728q";
    };

    propagatedBuildInputs = with pyPkgs; [
      (pyserial.overrideAttrs(o: {
        doInstallCheck = false;
      }))
      (libusb1.overrideAttrs(o: {
        doInstallCheck = false;
      }))
      pyDes
      ndeflib
    ];
  };
in with pkgs; pyPkgs.buildPythonPackage rec {
  name = "hydra-ci-example-python";
  inherit src;
  propagatedBuildInputs = with pyPkgs; [
    django
    nfcpy
  ];

  checkInputs = with pyPkgs; [
    pytest
    pytestrunner
    pytest-flake8
  ];

  meta.maintainers = [
    "Josef Kemetmueller <josef.kemetmueller@gmail.com>"
  ];
}
