import Sigma from "sigma";
import FileSaver from "file-saver";

export default function saveAsPNG(renderer, inputLayers) {
  const { width, height } = renderer.getDimensions();

  const pixelRatio = window.devicePixelRatio || 1;

  const tmpRoot = document.createElement("DIV");
  tmpRoot.style.width = `${width}px`;
  tmpRoot.style.height = `${height}px`;
  tmpRoot.style.position = "absolute";
  tmpRoot.style.right = "101%";
  tmpRoot.style.bottom = "101%";
  document.body.appendChild(tmpRoot);

  const tmpRenderer = new Sigma(renderer.getGraph(), tmpRoot, renderer.getSettings());

  tmpRenderer.getCamera().setState(renderer.getCamera().getState());
  tmpRenderer.refresh();

  const canvas = document.createElement("CANVAS");
  canvas.setAttribute("width", width * pixelRatio + "");
  canvas.setAttribute("height", height * pixelRatio + "");
  const ctx = canvas.getContext("2d");

  const canvases = tmpRenderer.getCanvases();
  const layers = inputLayers ? inputLayers.filter((id) => !!canvases[id]) : Object.keys(canvases);
  layers.forEach((id) => {
    ctx.drawImage(
      canvases[id],
      0,
      0,
      width * pixelRatio,
      height * pixelRatio,
      0,
      0,
      width * pixelRatio,
      height * pixelRatio,
    );
  });

  canvas.toBlob((blob) => {
    if (blob) FileSaver.saveAs(blob, "graph.png");

    tmpRenderer.kill();
    tmpRoot.remove();
  }, "image/png");
}

