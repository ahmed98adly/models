"""
-------------------------------------------------
MHub - run the SYBIL pipeline
-------------------------------------------------

-------------------------------------------------
Author: Ahmed Adly
Email:  ahmed.hassan@maastrichtuniversity.nl
-------------------------------------------------
"""

from ast import Module
import os, subprocess, shutil, json, csv
import pandas as pd
from mhubio.core import Instance, InstanceData, IO, Module, ValueOutput, Meta
from mhubio.modules.runner.ModelRunner import ModelRunner


@ValueOutput.Name('sybilscores')
@ValueOutput.Meta(Meta(key="value"))
@ValueOutput.Label('SybilRiskScore')
@ValueOutput.Type(float)
@ValueOutput.Description('Sybil Risk Scores for 6 years.')
class SybilScores(ValueOutput):
   pass


@ValueOutput.Name('sybilscores')
@ValueOutput.Meta(Meta(key="value"))
@ValueOutput.Label('SybilRiskScore')
@ValueOutput.Type(float)
@ValueOutput.Description('Sybil Risk Scores for 6 years.')
class RiskScoresloc(ValueOutput):
   pass


class SybilRunner(Module):
    
    @IO.Instance()
    @IO.Input('in_data', 'dicom:mod=ct',  the='input dicom chest ct')
    @IO.Output('risk_scores',  'sybil.csv', "csv", the='predicted cancer risk')
    @IO.OutputData('sybilscores', SybilScores, data='in_data', the='sybil scores')

    def task(self, instance: Instance, in_data: InstanceData, risk_scores: InstanceData, sybilscores: SybilScores) -> None: 
        
        # import sybil model
        from sybil import Serie, Sybil

        # Load a trained model
        model = Sybil("sybil_ensemble")

        # get dicom files for single instance
        dcm_images = [os.path.join(in_data.abspath, f) for f in os.listdir(in_data.abspath) if f.endswith('.dcm')]
    
        # Get risk scores
        serie = Serie(dcm_images)
        SybilScores.value = model.predict([serie])

        # save risk scores for 6 years for every instance
        df = pd.DataFrame({'Scores': SybilScores.value })
        df.to_csv(risk_scores.abspath, index=False)

        