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
  pyPkgs = getPythonVersion pkgs;
  nfcpy = pyPkgs.buildPythonPackage rec {
    pname = "nfcpy";
    version = "0.13.5";
    src = pkgs.fetchFromGitHub rec {
      owner = pname;
      repo = pname;
      rev = "v${version}";
      sha256 = "0n99saanbv2w3665ki675b66m517pnqg9m17jbcqgvfs6j1nbnp0";
    };
    propagatedBuildInputs = with pkgs.python.pkgs; [
      pyserial
      libusb1
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
