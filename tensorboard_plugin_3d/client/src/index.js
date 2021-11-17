import materialUIMachineOptions from 'itk-viewer-material-ui/src/materialUIMachineOptions'
import modifiedCreateInterface from './main'

const uiMachineOptions = { ...materialUIMachineOptions }

const uiMachineActions = { ...uiMachineOptions.actions }
uiMachineActions.createInterface = modifiedCreateInterface

uiMachineOptions.actions = uiMachineActions

const container = document.querySelector('.content')
const ipfsImage = new URL("https://data.kitware.com/api/v1/file/564a65d58d777f7522dbfb61/download/data.nrrd")
window.itkVtkViewer.createViewer(container,
  {
  image: ipfsImage,
  rotate: false,
  config: { uiMachineOptions },
  })
