####################################################################################

**ADDENDUM: Based on the initial reviews received from the reviewers (Smoke-Test), a newer version of our artefact has been published. You can go to the old link and navigate to the newer version or use the link https://doi.org/10.5281/zenodo.15373266 for the latest version. The new version additionally contains a Docker image of the STORM model checker and some troubleshooting instructions. Files relating to GALTOSM tool remain unaltered.** 

####################################################################################


This artifact accompanies the tool paper titled “GALTOSM: A Graph and Logic Transformation Based Toolkit for Software Model Checking”, submitted to `ATVA 2025` with submission number `5790`. It includes all necessary source codes and a reproduction package supporting the claims made in the paper. Reproducing the case studies requires model checking tools such as `CADP (version 2024-k ”Eindhoven”)` and `STORM (version 1.9.0)`. Although the toolkit also supports integration with PRISM and mCRL2, these tools are not directly involved in the results claimed in the paper.

There are no strict hardware requirements to run the toolkit; machines with higher capacity can process larger models, while lower-capacity systems may be limited to smaller ones. We have carried out all the case study experiments in an `Ubuntu 22.04.5 LTS` machine with `CPU Intel® Xeon(R) Silver 4314 CPU @ 2.40GHz × 64 and 640.0 GiB, 1TB, primary and SSD memory`.

This artifact contains a `README.txt` file and a `READ DIRECTORY.pdf` file in every directory for better understanding. The source code is well commented and the README files describe the alignment of the source code with the objective and the functionalities provided by the tool.

The Link to the Zenodo repository is https://doi.org/10.5281/zenodo.15332059

SHA256 checksum value of the zipped artifact is `0971bebeb6eb1a5317f752e63b5ca91ad9e2a586a64214e077e4c319417981ef`

The Github repository also contains a detailed handbook to using our tool GALTOSM and the results (tables and graphs) for your reference.

<!-- Note: The subdirectory `Sample_Artifact_GALTOSM` contains some sample files and strctures to help reviewers get an overview, sanity-check, and to check small fragments of the case studies in the paper which are smaller in size and requires less times to compile and model check. It also contains the codes for GALTOSM which can be easily evaluated without requiring the user to download the entire artefact. -->
