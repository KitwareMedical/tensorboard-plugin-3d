import React, { useEffect, useState } from 'react'
import { useActor } from '@xstate/react'
import { Button, LinearProgress, TextField } from '@mui/material'
import { ArrowBack, ArrowForward, FirstPage, LastPage } from '@mui/icons-material'
import {
  encodeScijsArray, fetchJSON, saveStateSettings,
  updateLabelSettings, updateStateSettings
} from './utils'
import './style.css'
import { debounce } from 'lodash'
import createViewer from 'itk-vtk-viewer/src/createViewer'

function ImageSelector(props) {
  const { service } = props
  const [state, send] = useActor(service)
  const [imageCount, setImageCount] = useState({current: 1, total: 1})
  const [changingImage, setChangingImage] = useState(false);
  const lastAddedData = state.context.layers.lastAddedData;
  const name = state.context.images.selectedName;
  const component = state.context.images.selectedComponent;
  const actorContext = state.context.images.actorContext.get(name)

  useEffect(() => {
    if (actorContext && window.loading) {
      toggleProgressCircle(false)
    }
  }, [actorContext])

  useEffect(async() => {
    const counts = await fetchJSON(`../tensorboard_plugin_3d/images/count`);
    setImageCount(counts);
  }, [])

  useEffect(() => {
    if (actorContext?.labelImageName && actorContext?.labelImageToggleWeight)
      updateLabelSettings(name, actorContext.labelImageToggleWeight, send)
  }, [actorContext?.labelImageName])

  useEffect(() => {
    if (name && component >= 0 && actorContext?.colorRanges) {
      const colorRange = actorContext.colorRanges.get(component);
      updateStateSettings(name, component, colorRange, send);
    }
  }, [name, component, actorContext])

  const toggleProgressCircle = (state) => {
    window.loading = state
    let elem = document.getElementById('loading')
    elem.style.display = state ? 'block' : 'none'
  }

  const changeImage = async (idx) => {
    if (idx < 1)
      idx = 1
    if (idx > imageCount.total)
      idx = imageCount.total

    saveStateSettings(state.context);
    const params = new URLSearchParams({idx})
    setChangingImage(true);
    const img_data = await fetchJSON(`../tensorboard_plugin_3d/images/current?${params}`)
    .then(response => {
      let image_data = {image: encodeScijsArray(response.image)}
      if (response.label) {
        image_data.labelImage = encodeScijsArray(response.label)
      }
      return image_data
    })
    toggleProgressCircle(true)
    createViewer(
      document.querySelector('.content'),
      {
        ...img_data,
        rotate: state.context.main.rotateEnabled,
        config: { ...state.context },
      }).finally(() => setChangingImage(false))
  }

  const debouncedChangeImage = debounce((idx) => {changeImage(idx)}, [500])

  const handleChange = (value) => {
    value = Math.max(Math.min(value, imageCount.total), 1)
    const diff = value - imageCount.current
    if (diff) {
      setImageCount({...imageCount, current: imageCount.current + diff})
      debouncedChangeImage(imageCount.current + diff)
    }
  }

  return (
    <div className={(!lastAddedData || imageCount.total < 2) ? "hidden" : "imageSelectorContainer"}>
      <div className='imageToggle'>
      <Button
          variant="contained"
          size="small"
          style={{marginRight: '3px'}}
          className={"arrowButtons"}
          disabled={imageCount.current === 1 || changingImage}
          onClick={() => {
            setImageCount({...imageCount, current: 1})
            debouncedChangeImage(1)
          }}
        >
          <FirstPage />
        </Button>
        <Button
          variant="contained"
          size="small"
          style={{marginRight: '3px'}}
          className={"arrowButtons"}
          disabled={imageCount.current === 1 || changingImage}
          onClick={() => {
            setImageCount({...imageCount, current: imageCount.current-1})
            debouncedChangeImage(imageCount.current-1)
          }}
        >
          <ArrowBack />
        </Button>
        Image
        <TextField
          type="number"
          className="imageInput"
          InputLabelProps={{
            shrink: true
          }}
          variant="filled"
          size="small"
          margin="dense"
          disabled={changingImage}
          value={imageCount.current}
          onChange={(e) => {handleChange(e.target.value)}}
        />
        of {imageCount.total}
        <Button
          variant="contained"
          size="small"
          style={{marginLeft: '3px'}}
          className={"arrowButtons"}
          disabled={imageCount.current === imageCount.total || changingImage}
          onClick={() => {
            setImageCount({...imageCount, current: imageCount.current+1})
            debouncedChangeImage(imageCount.current+1)
          }}
        >
          <ArrowForward />
        </Button>
        <Button
          variant="contained"
          size="small"
          style={{marginLeft: '3px'}}
          className={"arrowButtons"}
          disabled={imageCount.current === imageCount.total || changingImage}
          onClick={() => {
            setImageCount({...imageCount, current: imageCount.total})
            debouncedChangeImage(imageCount.total)
          }}
        >
          <LastPage />
        </Button>
      </div>
      <div className={changingImage ? "" : "hidden"}>
        <LinearProgress color="inherit" />
      </div>
    </div>
  )
}

export default ImageSelector
