[
  (self: super: {
    yq = super.stdenv.mkDerivation {
      pname = "yq";
      version = "4.44.3";

      src = super.fetchurl {
        url =
          if super.stdenv.hostPlatform.isDarwin
          then "https://github.com/mikefarah/yq/releases/download/v4.44.3/yq_darwin_arm64"
          else "https://github.com/mikefarah/yq/releases/download/v4.44.3/yq_linux_amd64";
        sha256 =
          if super.stdenv.hostPlatform.isDarwin
          then "sha256-VZpZTvem68W4Gme3cX+zrM7dJm2Pp9g1Laf+yeRj9Is="
          else "a2c097180dd884a8d50c956ee16a9cec070f30a7947cf4ebf87d5f36213e9ed7";
      };

      phases = ["installPhase"];

      installPhase = ''
        mkdir -p $out/bin
        cp $src $out/bin/yq
        chmod +x $out/bin/yq
      '';

      meta = {
        description = "A lightweight and portable command-line YAML processor";
        homepage = "https://github.com/mikefarah/yq";
        license = super.lib.licenses.mit;
        maintainers = [];
      };
    };
  })

  (self: super: {
    make = super.make.overrideAttrs (oldAttrs: rec {
      pname = "make";
      version = "4.4.1";

      src = super.fetchurl {
        url = "https://ftp.gnu.org/gnu/make/make-${version}.tar.gz";
        sha256 = "ea9b4f68efb6046f692b8f6a10e9798f4c6b2be14225b89c93709c1042caf8a9";
      };

      nativeBuildInputs = oldAttrs.nativeBuildInputs or [] ++ [super.gnum4];

      buildInputs = oldAttrs.buildInputs or [] ++ [super.gnum4];

      configureFlags = oldAttrs.configureFlags or [] ++ ["--disable-nls"];

      meta = with super.lib; {
        description = "GNU Make is a tool which controls the generation of executables and other non-source files of a program from the program's source files.";
        homepage = "https://www.gnu.org/software/make/";
        license = licenses.gpl3Plus;
        maintainers = [];
      };
    });
  })
]
