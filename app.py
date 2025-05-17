#!/usr/bin/env python3

import aws_cdk as cdk

from nba_dfs_demo_cdk.nba_dfs_demo_cdk_stack import NbaDfsDemoCdkStack


app = cdk.App()
NbaDfsDemoCdkStack(app, "NbaDfsDemoCdkStack")

app.synth()
