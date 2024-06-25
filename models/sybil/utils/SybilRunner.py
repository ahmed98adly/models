"""
-------------------------------------------------
MHub - run the SYBIL pipeline
-------------------------------------------------

-------------------------------------------------
Author: Ahmed Adly
Email:  ahmed.hassan@maastrichtuniversity.nl
-------------------------------------------------
"""

import os, subprocess, shutil, json, csv
import pandas as pd
from mhubio.core import Instance, InstanceData, IO
from mhubio.modules.runner.ModelRunner import ModelRunner

class SybilRunner(ModelRunner):
    
    @IO.Instance()
    @IO.Input('in_data', 'dicom:mod=ct',  the='input dicom chest ct')
    @IO.Output('risk_scores',  'sybil.csv', "csv:type=scores", the='predicted cancer risk')

    def task(self, instance: Instance, in_data: InstanceData, risk_scores: InstanceData) -> None:
        
        # import sybil model
        from sybil import Serie, Sybil

        # Load a trained model
        model = Sybil("sybil_ensemble")

        # get dicom files for single instance
        dcm_images = [os.path.join(in_data.abspath, f) for f in os.listdir(in_data.abspath) if f.endswith('.dcm')]
    
        # Get risk scores
        serie = Serie(dcm_images)
        scores = model.predict([serie])
        
        # save risk scores for 6 years for every instance
        df = pd.DataFrame({'Scores': scores})
        df.to_csv(risk_scores.abspath, index=False)

        