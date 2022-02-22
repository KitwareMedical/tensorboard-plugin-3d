import materialUIMachineOptions from 'itk-viewer-material-ui/src/materialUIMachineOptions'
import modifiedCreateInterface from './main'
import { encodeScijsArray, fetchJSON } from './utils'

const uiMachineOptions = { ...materialUIMachineOptions }

const uiMachineActions = { ...uiMachineOptions.actions }
uiMachineActions.createInterface = modifiedCreateInterface

uiMachineOptions.actions = uiMachineActions

const container = document.querySelector('.content')

async function createViewer() {
  const img_data = await fetchJSON('../tensorboard_plugin_3d/images/current').then(response => {
    let image_data = {image: encodeScijsArray(response.image)}
    if (response.label) {
      image_data.labelImage = encodeScijsArray(response.label)
    }
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
