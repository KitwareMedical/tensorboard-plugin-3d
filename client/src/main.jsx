import React from 'react'
import ReactDOM from 'react-dom'
import 'itk-viewer-material-ui/src/style.css'
import CollapseUIButton from 'itk-viewer-material-ui/src/CollapseUIButton'
import Panel from 'itk-viewer-material-ui/src/Panel'
import MainInterface from 'itk-viewer-material-ui/src/Main/MainInterface'
import ImagesInterface from 'itk-viewer-material-ui/src/Images/ImagesInterface'
import ImageSelector from './ImageSelector'
import WidgetsInterface from 'itk-viewer-material-ui/src/Widgets/WidgetsInterface'
import './style.css'
import LayersInterface from 'itk-viewer-material-ui/src/Layers/LayersInterface'

function modifiedCreateInterface(context) {
  context.viewContainers = new Map()
  const viewContainer = document.createElement('div')
  viewContainer.setAttribute('class', 'viewContainer')
  context.viewContainers.set('volume', viewContainer)
  viewContainer.appendChild(context.renderingViewContainers.get('volume'))
  context.rootContainer.appendChild(viewContainer)

  if (!context.uiContainer) {
    const uiContainer = document.createElement('div')
    uiContainer.setAttribute('class', 'uiContainer')
    context.uiContainer = uiContainer
  }

  context.rootContainer.appendChild(context.uiContainer)
  if (!context.uiGroups) {
    context.uiGroups = new Map()
  }

  ReactDOM.render(
    <React.StrictMode>
      <CollapseUIButton service={ context.service }/>
      <Panel service={ context.service }>
        <MainInterface />
        <ImageSelector />
        <LayersInterface />
        <WidgetsInterface />
        <ImagesInterface />
      </Panel>
    </React.StrictMode>,
    context.uiContainer
  )
}

export default modifiedCreateInterface