{
  description = "pinger cli";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix.url = "github:nix-community/poetry2nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    poetry2nix,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        overlays = import ./overlays;
        pkgs = import nixpkgs {inherit system overlays;};
        inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication;
        myPythonApp = mkPoetryApplication {
          projectDir = ./.;
        };
      in {
        packages.default = myPythonApp;
        apps.default = {
          type = "app";
          program = "${myPythonApp}/bin/pinger";
        };
        devShells.default = pkgs.mkShell {
          shellHook = ''
            if command -v poetry >/dev/null 2>&1; then
              VENV_PATH=$(poetry env info --path 2>/dev/null)
              if [ -d "$VENV_PATH" ]; then
                echo "Activating Poetry virtual environment from $VENV_PATH"
                . "$VENV_PATH/bin/activate"
              else
                echo "No Poetry environment found. Run 'poetry install' to create one."
              fi
            else
              echo "Poetry is not installed."
            fi
          '';
          buildInputs = with pkgs; [
            docker-compose
            python312
            gnumake
            docker
            poetry
            direnv
            cmake
            yq
          ];
        };
      }
    );
}
