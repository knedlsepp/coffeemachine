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
  pyPkgs = getPythonVersion pkgs;
in with pkgs; pyPkgs.buildPythonPackage rec {
  name = "coffeemachine";
  inherit src;
  propagatedBuildInputs = with pyPkgs; [
    django
    pandas
    pyscard
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
