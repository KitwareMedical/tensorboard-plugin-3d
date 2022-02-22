import ndarraypack from 'ndarray-pack'
import {isEmpty} from 'lodash'


export async function fetchJSON(url, params=null) {
  if (!params) {
    params = {}
  }
  const response = await fetch(url, params);
  if (!response.ok) {
    return null;
  }
  const data = response.json();
  return data;
}


export function encodeScijsArray(array){
  const ndarray = ndarraypack(array)
  const encoded = {
    _rtype: 'ndarray',
    _rdtype: ndarray.dtype,
    _rshape: ndarray.shape,
    _rvalue: ndarray.data,
  }
  return encoded
}


function preproccessActorContext(actorContext) {
  let ac = {
    blendMode: actorContext.blendMode,
    colorMap: actorContext.colorMaps.get(0),
    colorRange: actorContext.colorRanges.get(0),
    gradientOpacity: actorContext.gradientOpacity,
    gradientOpacityScale: actorContext.gradientOpacityScale,
    interpolationEnabled: actorContext.interpolationEnabled,
    labelImageName: actorContext.labelImageName,
    piecewiseFunctionGaussians: actorContext.piecewiseFunctionGaussians.get(0),
    piecewiseFunctions: actorContext.piecewiseFunctions.get(0),
    shadowEnabled: actorContext.shadowEnabled,
    volumeSampleDistance: actorContext.volumeSampleDistance
  }

  if (actorContext.labelImageName) {
    ac['labelImageBlend'] = actorContext.labelImageBlend;
    ac['labelImageToggleWeight'] = actorContext.labelImageToggleWeight;
    ac['lookupTable'] = actorContext.lookupTable;
    ac['selectedLabel'] = actorContext.selectedLabel;
  }

  return ac
}


export async function saveStateSettings(context) {
  const {
    annotationsEnabled,
    axesEnabled,
    backgroundColor,
    slicingPlanes,
    xSlice,
    ySlice,
    zSlice,
    viewMode
  } = context.main;
  const {actorContext} = context.images;

  const data = {
    annotationsEnabled,
    axesEnabled,
    backgroundColor,
    xSlice,
    ySlice,
    zSlice,
    viewMode,
    slicingPlanes,
    actorContext: preproccessActorContext(actorContext.get('Image'))
  }

  const params = {
    method: 'PUT',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify(data)
  }

  await fetchJSON('../tensorboard_plugin_3d/saveState', params);
}


export async function updateLabelSettings(name, labelImageToggleWeight, send) {
  const state = await fetchJSON('../tensorboard_plugin_3d/fetchState');
  if (isEmpty(state))
    return

  if (state.actorContext?.labelImageToggleWeight)
    labelImageToggleWeight = state.actorContext.labelImageToggleWeight;

  if (state.actorContext.labelImageBlend) {
    send({
      type: 'LABEL_IMAGE_BLEND_CHANGED',
      data: {name, labelImageBlend: state.actorContext.labelImageBlend}
    })
  }
  if (state.actorContext?.selectedLabel) {
    send({
      type: 'LABEL_IMAGE_SELECTED_LABEL_CHANGED',
      data: {name, selectedLabel: state.actorContext.selectedLabel}
    })
  }
  if (state.actorContext?.lookupTable) {
    send({
      type: 'LABEL_IMAGE_LOOKUP_TABLE_CHANGED',
      data: {name, lookupTable: state.actorContext.lookupTable}
    })
  }
}


export async function updateStateSettings(name, component, send) {
  const state = await fetchJSON('../tensorboard_plugin_3d/fetchState');
  if (isEmpty(state))
    return

  if (!state.annotationsEnabled)
    send('TOGGLE_ANNOTATIONS')
  if (state.axesEnabled)
    send('TOGGLE_AXES')
  if (!state.actorContext.shadowEnabled)
    send({type: 'TOGGLE_IMAGE_SHADOW', data: name})
  if (!state.actorContext.interpolationEnabled)
    send({type: 'TOGGLE_IMAGE_INTERPOLATION', data: name})

  send({type: 'SET_BACKGROUND_COLOR', data: state.backgroundColor})
  send({type: `X_SLICE_CHANGED`, data: state.xSlice})
  send({type: `Y_SLICE_CHANGED`, data: state.ySlice})
  send({type: `Z_SLICE_CHANGED`, data: state.zSlice})
  send({type: 'SLICING_PLANES_CHANGED', data: state.slicingPlanes})
  send({type: 'VIEW_MODE_CHANGED', data: state.viewMode})
  send({
    type: 'IMAGE_COLOR_MAP_CHANGED',
    data: {
      name,
      component: component,
      colorMap: state.actorContext.colorMap
    }
  })
  send({
    type: 'IMAGE_BLEND_MODE_CHANGED',
    data: {name, blendMode: state.actorContext.blendMode}
  })
  send({
    type: 'IMAGE_COLOR_RANGE_CHANGED',
    data: {
      name,
      component: component,
      range: state.actorContext.colorRange
    }
  })
  send({
    type: 'IMAGE_GRADIENT_OPACITY_SCALE_CHANGED',
    data: {name, gradientOpacityScale: state.actorContext.gradientOpacityScale}
  })
  send({
    type: 'IMAGE_GRADIENT_OPACITY_CHANGED',
    data: {name, gradientOpacity: state.actorContext.gradientOpacity}
  })
  send({
    type: 'IMAGE_VOLUME_SAMPLE_DISTANCE_CHANGED',
    data: {name, volumeSampleDistance: state.actorContext.volumeSampleDistance}
  })
  send({
    type: 'IMAGE_PIECEWISE_FUNCTION_GAUSSIANS_CHANGED',
    data: {
      name,
      component: component,
      gaussians: state.actorContext.piecewiseFunctionGaussians
    }
  })
  send({
    type: 'IMAGE_PIECEWISE_FUNCTION_CHANGED',
    data: {
      name,
      component: component,
      range: state.actorContext.piecewiseFunctions.range,
      nodes: state.actorContext.piecewiseFunctions.nodes
    }
  })
}