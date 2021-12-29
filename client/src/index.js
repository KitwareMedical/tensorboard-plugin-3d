import materialUIMachineOptions from 'itk-viewer-material-ui/src/materialUIMachineOptions'
import modifiedCreateInterface from './main'
import ndarraypack from 'ndarray-pack'

const uiMachineOptions = { ...materialUIMachineOptions }

const uiMachineActions = { ...uiMachineOptions.actions }
uiMachineActions.createInterface = modifiedCreateInterface

uiMachineOptions.actions = uiMachineActions

const container = document.querySelector('.content')

async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    return null;
  }
  const data = response.json();
  return data;
}

function encodeScijsArray(array){
  const encoded = {
    _rtype: 'ndarray',
    _rdtype: array.dtype,
    _rshape: array.shape,
    _rvalue: array.data,
  }
  return encoded
}

async function createViewer() {
  const img_data = await fetchJSON('../tensorboard_plugin_3d/images').then(response => {
    let image_data = {image: encodeScijsArray(ndarraypack(response.images[0].array))}
    if (response.images.length > 1) {
      image_data.labelImage = encodeScijsArray(ndarraypack(response.images[1].array))
    }
    response.images.forEach((img) => {
      encodeScijsArray(ndarraypack(img.array))
    })
    return image_data
  })
  window.itkVtkViewer.createViewer(container,
    {
      ...img_data,
      rotate: false,
      config: { uiMachineOptions },
    })
}
createViewer()
