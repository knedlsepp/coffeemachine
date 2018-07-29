{
  nixpkgs ? (builtins.fetchGit {
    url = https://github.com/NixOS/nixpkgs-channels.git;
    ref = "nixos-18.03";
  })
, getPythonVersion ? p: p.python3Packages
, source ? fetchGit ./.
}:

let
  pkgs = import nixpkgs { };
  pyPkgs = getPythonVersion pkgs;
in pyPkgs.buildPythonPackage rec {
  name = "coffee-machine";
  src = if ! pkgs.lib.inNixShell then null else source;
  propagatedBuildInputs = with pyPkgs; [
    django
  ];
}