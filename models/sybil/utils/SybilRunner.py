"""
-------------------------------------------------
MHub - run the SYBIL pipeline
-------------------------------------------------

-------------------------------------------------
Author: Ahmed Adly
Email:  ahmed.hassan@maastrichtuniversity.nl
-------------------------------------------------
"""

import os, subprocess, shutil, json
from mhubio.core import Instance, InstanceData, IO, Module, ValueOutput, Meta


@ValueOutput.Name('sybilscores')
@ValueOutput.Meta(Meta(key="value"))
@ValueOutput.Label('sybilscores')
@ValueOutput.Type(float)
@ValueOutput.Description('Sybil Risk Scores for 6 years.')
class SybilScores(ValueOutput):
   pass


class SybilRunner(Module):
    
    @IO.Instance()
    @IO.Input('in_data', 'dicom:mod=ct',  the='input dicom chest ct')
    @IO.OutputData('sybilscores', SybilScores, data='in_data', the='sybil scores')

    def task(self, instance: Instance, in_data: InstanceData, sybilscores: SybilScores) -> None: 
        
        # import sybil model
        from sybil import Serie, Sybil

        # Load a trained model
        model = Sybil("sybil_ensemble")

        # get dicom files for single instance
        dcm_images = [os.path.join(in_data.abspath, f) for f in os.listdir(in_data.abspath) if f.endswith('.dcm')]
    
        # Get risk scores and save it into json file
        serie = Serie(dcm_images)
        SybilScores.value = model.predict([serie])


        