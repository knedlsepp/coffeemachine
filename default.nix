{ nixpkgs ? (builtins.fetchGit {
    url = git://github.com/NixOS/nixpkgs-channels;
    ref = "nixos-18.03";
    rev = "08d245eb31a3de0ad73719372190ce84c1bf3aee";
  })
, getPythonVersion ? (p: p.python3Packages)
, src ? builtins.fetchGit ./.
}:
let
  overlays = [ ];
  pkgs = import nixpkgs { inherit overlays; config = { }; };
  pyscard = pyPkgs.pyscard.overrideAttrs(o: rec {
    preBuild = ''
      # Getting rid of commit: https://github.com/LudovicRousseau/pyscard/commit/37b6997d05ee9feae41ad53c0189474fd23fb3be.patch
      substituteInPlace smartcard/CardMonitoring.py --replace "self.stopEvent.set()" "pass"
    '';
  });
  smbus2 = pyPkgs.buildPythonPackage rec {
    name = "smbus2-${version}";
    version = "0.2.1";
    src = pkgs.fetchurl {
      url = "mirror://pypi/s/smbus2/${name}.tar.gz";
      sha256 = "0axzrb1b20vjsp02ppz0x28pwn8gvx3rzrsvkfbbww26wzzl7ndq";
    };
  };
  pandas = pyPkgs.pandas.overrideAttrs(o: rec {
    doCheck = false;
	doInstallCheck = false;
  });

  pyPkgs = getPythonVersion pkgs;
in with pkgs; pyPkgs.buildPythonPackage rec {
  name = "coffeemachine";
  inherit src;
  propagatedBuildInputs = with pyPkgs; [
    django_2_0
    pandas
    pyscard
    smbus2
  ];
  doCheck = false; # TODO!
  checkInputs = with pyPkgs; [
    pytest
    pytest-django
    pytestrunner
    pytest-flake8
  ];

  meta.maintainers = [
    "Josef Kemetmueller <josef.kemetmueller@gmail.com>"
  ];
}
