# TAXIPP documentation

> Note: this documentation is being written.

openfisca-france-indirect-taxation is the [Institut des Politiques Publique](www.ipp.eu)'s microsimulation software.

It is published under the [GNU Affero General Public License version 3.0](http://www.gnu.org/licenses/agpl-3.0.html).

## About this documentation

This documentation is built with the excellent [GitBook](https://github.com/GitbookIO/gitbook) tool
(see [GitBook documentation](http://help.gitbook.com/)).

It is written in [Markdown](http://help.gitbook.com/format/markdown.html)
and the source is hosted on this GitHub repository:
[ipp/taxipp](https://git.framasoft.org/ipp/taxipp).

### Collaborative editing

Everybody can participate to the redaction of the documentation.

On each page is a link named "Edit this page".
Just click on it and you'll jump on GitHub on the Markdown source file of the page.
Then edit the file as explained on this GitHub documentation page:
[editing-files-in-another-user-s-repository](https://help.github.com/articles/editing-files-in-another-user-s-repository/).

Then save the file and create a [pull request](https://help.github.com/articles/creating-a-pull-request/) which will be
accepted if relevant.

### Build it yourself

If you'd like to build it by yourself, here are the steps.

```
git clone git@git.framasoft.org:ipp/taxipp.git
npm install
```

Then you can either build the documentation or launch a local HTTP server with watch mode:

```
npm run build
or
npm run watch
```

> With watch mode, open http://localhost:2050/ in your browser once the first build is done.

### Deploy (for maintainers)

To deploy the built documentation
(you must be authorized to push to [openfisca/openfisca-france-indirect-taxation](https://github.com/openfisca/openfisca-france-indirect-taxation)):

```
npm run publish
```

Then on the server, the first time:

```bash
git clone https://github.com/openfisca/openfisca-france-indirect-taxation.git --branch gitbook-static taxipp-gitbook-static
```

The next times:

```bash
cd taxipp-gitbook-static
git fetch
git reset --hard origin/gitbook-static
```
