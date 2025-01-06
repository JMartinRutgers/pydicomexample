import pydicom
import plotly.graph_objects as go
from ipywidgets import interact, IntSlider
import numpy as np

path_to_dicom_file = '0002.DCM'

try:
    ds = pydicom.dcmread(path_to_dicom_file)
    pixels_volume = ds.pixel_array
    nb_frames = len(pixels_volume)
    r, c = pixels_volume[0].shape

    # Create frames for animation
    frames = [go.Frame(data=[go.Surface(
        z=(k + 1) * np.ones((r, c)),
        surfacecolor=pixels_volume[k],
        colorscale='gray',
        cmin=0, cmax=255
    )],
        name=str(k)
    ) for k in range(nb_frames)]

    # Initial surface plot
    initial_surface = go.Surface(
        z=np.ones((r, c)),
        surfacecolor=pixels_volume[0],
        colorscale='gray',
        cmin=0, cmax=255
    )

    # Layout for the figure
    layout = go.Layout(
        title='DICOM Viewer',
        scene=dict(
            zaxis=dict(range=[0, nb_frames + 1], autorange=False)
        ),
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 100, 'redraw': True},
                                    'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True},
                                      'mode': 'immediate',
                                      'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]
    )

    # Create the figure
    fig = go.Figure(data=[initial_surface], layout=layout, frames=frames)

    # Display the figure
    fig.show()

    # Function to interact with the slider
    def view_frame(frame):
        fig.update_traces(z=(frame + 1) * np.ones((r, c)), surfacecolor=pixels_volume[frame])

    # Interactive slider
    interact(view_frame, frame=IntSlider(min=0, max=nb_frames-1, step=1, value=0))

except FileNotFoundError:
    print(f"Error: File '{path_to_dicom_file}' not found. Please check the file path and try again.")

