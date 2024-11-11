# Resume-md

This project allows you to write and maintain your resume in markdown. GitHub
Actions is used to generate stylized PDF and HTML files based on `resume.md`
and `style.css`. The stylized files are found as outputs in the `Releases`
section, the HTML file is also deployed as a static website using GitHub Pages.

This project is useful for anyone looking to create a professional-looking
resume quickly and easily, and is especially beneficial for those with
technical backgrounds who are familiar with markdown. With this project, you
can focus on the content of your resume rather than worrying about formatting
and deployment.


## Usage


### GitHub

1. Generate a new project using this repository as a template. **Make sure to include all branches!**
2. Enable Read/Write Workflow permissions under `Settings` -> `Actions` for Pages deployment.
3. Edit the `resume.md` file with your resume content using Markdown.
4. Commit and push the changes.
5. Wait for the GitHub Actions to run. This will generate the PDF and HTML files and deploy
the HTML file as a static website.
6. Access the PDF and HTML in the `Releases` section.
7. Access your resume as a static website by going to `https://<your-github-username>.github.io/<repository-name>`.


### Local

`Resume-md` uses [`nix`](https://www.nixos.org) to manage all dependencies and
to produce build outputs. As a result, any machine with `nix` installed can run
a simple build command to produce the stylized resumes.
```shell
nix build
```

This will place the stylized files along side the original markdown file in
`result/resume/`:
```shell
 result
└──  resume
    ├──  resume.html
    ├──  resume.md
    └──  resume.pdf
```

## GitHub Pages

GitHub Pages is used to deploy the stylized HTML file as a static site. For this to work,
the Workflow Permissions MUST be set to read/write and the repository must be public or
the user a pro user. If you forked this repository or didn't copy the branches during generation,
you will need to point the pages deployment to the `gh-pages` branch under the `Pages` settings.


## Customization

You can customize the stylized PDF and HTML output by editing `style.css`.


### Default Look

![demo](./demo.png)


## Validation Process in CI/CD Pipeline

The CI/CD pipeline includes validation steps to ensure the generated HTML and PDF files are properly formatted. The validation process is as follows:

1. **HTML Validation**: The `html-validator-cli` tool is used to validate the generated HTML file. This ensures that the HTML file is properly formatted and adheres to web standards.
2. **PDF Validation**: The `pdfinfo` tool from the `poppler-utils` package is used to validate the generated PDF file. This ensures that the PDF file is properly formatted and contains the expected content.

These validation steps are included in the `generate` job of the GitHub Actions workflow (`.github/workflows/generate.yaml`).
W.I.P

## Credits

Originally inspired by [vidluther's project](https://github.com/vidluther/markdown-resume).
