{
  description = "Build your resume with markdown";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let

        pkgs = import nixpkgs {
          inherit system;
          config = {
            permittedInsecurePackages = [ "openssl-1.1.1w" ];
          };
        };

        buildInputs = with pkgs; [
          pandoc
          wkhtmltopdf-bin
          vnu-jar  # Replacing html-validator-cli with vnu-jar
          poppler-utils
        ];

        buildPhase = ''
          pandoc resume.md \
          -t html -f markdown \
          -c style.css --self-contained \
          -o resume.html

          wkhtmltopdf --enable-local-file-access \
          resume.html \
          resume.pdf

          java -jar $(which vnu.jar) resume.html  # HTML validation with vnu-jar

          pdfinfo resume.pdf
        '';

      in with pkgs; {

        packages = {
          default = stdenvNoCC.mkDerivation {
            inherit buildInputs buildPhase;
            name = "resume_md";
            src = ./.;
            installPhase = ''
              mkdir -p $out/resume
              cp resume.* $out/resume/
            '';
          };
        };

        checks = {
          default = stdenvNoCC.mkDerivation {
            inherit buildInputs buildPhase;
            name = "resume-md checks";
            src = ./.;
            installPhase = ''
              mkdir -p $out
            '';
          };
        };

        devShell = pkgs.mkShell {
          inherit buildInputs;
        };
      });
}
