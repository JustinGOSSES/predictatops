## A Supervised Machine-Learning Approach to Stratigraphic Surface Picking in Well Logs from the Mannville Group of Alberta, Canada
Gosses, Justin <br/>
1015 Aurora Street <br/>
Houston, Texas 77009<br/>
Jgosses82@gmail.com<br/>
<br/>
Zhang, Licheng<br/>
CCG<br/>
4610 Tilbury Trl.<br/>
Richmond, TX 77407<br/>
Licheng.zhang9@gmail.com<br/>
<br/>
<br/>
<b>Abstract</b><br/>
Variation in where stratigraphic surfaces are interpreted in well logs can significantly impact oil and gas resource calculations. Generating stratigraphic picks in hundreds of wells logs can take a geologist weeks to months. We propose a method for how supervised machine-learning can be used to extend human-generated well log picks to new wells, assuming a highly penetrated area where most depositional variance is captured in a training dataset. We use an open dataset of 2193 wells from the Mannville Group in Alberta Canada [Wynne et al., 1995] and our code is open-source [Gosses and Zhang, 2018]. 
<br/>
<br/>
Curve matching approaches, while useful for lithologic correlation, are abandoned due to the difficulty of getting those methods to deal effectively with local controls on deposition or controls whose expression changes spatially. Instead, features are created to mimic the visual comparisons geologists make while correlating cross-sections but at a lower level of observation, letting the machine-learning algorithm, XGBoost, combine features and assign weights in order to reach higher-order conclusions. For each depth point, features are created using GR, ILD, DPHI , NPHI curve values at above, below, and around that depth point. Other features are generated from known picks in neighboring training wells, curve data features from neighboring wells, location, and summary descriptions of each full well. To address class imbalances that result from trying to predict one depth in a well of thousands of depth points, we create class labels for depth points at the pick, within 0.5 meters, above 5 meters, below 5 meters, and outside that range. Less than 15% of the depth points outside of the 5 meters range are kept for training, and two machine learning models are employed in sequence. The first for class prediction. The second to examine the depths labeled as either at the pick or within 0.5 meters and pick the best candidate in each well via regression.
<br/>
<br/>
For the top McMurray pick, absolute mean errors are similar to that of a geologist new to the area mimicking the picking style of a geologist experienced with that formation. This type of approach may be useful in evaluation of nearby acreage, extending interpretation to infill wells, and quickly generating multiple probable picks in each well for monte carlo simulations. 
<br/>
REFERENCES
<br/>
Wynne, D.A., Attalla, M., Berezniuk, T., Brulotte, M., Cotterill, D.K., Strobl, R. and Wightman, D. (1995): Athabasca Oil Sands data McMurray/Wabiskaw oil sands deposit - electronic data; Alberta Research Council, ARC/AGS Special Report 6. http://ags.aer.ca/publications/SPE_006.html
<br/><br/>
Gosses, J.C. and Licheng, Z., (2018): StratPickSupML; DOI: 10.5281/zenodo.1450597. https://github.com/JustinGOSSES/StratPickSupML/
