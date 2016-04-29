
#include <PID_v1.h> 
///////define parts/////////
#define enablePin  52 
#define encoderRight  0
#define encoderLeft 1
#define controlLed 13
#define echoPin 30
#define trigPin 31

#define motorRFA 7  // sag motor sari pin//sag ileri aktif
#define motorRBA 6  // sag motor siyah pin
#define motorLBA 5  // sol motor kirmizi pin
#define motorLFA 4  // sol motor siyah pin
#define motorSpeed 125
volatile int hitsRight = 0;
volatile int hitsLeft = 0;
long distance;
int raspMessage,roundDirection,var, zot, temp1, 5IndexILj2EEESt5dequeIS3_SaIS3_EEESt4lessItESaISt4pairIKtS7_EEE8key_compEv _ZNK3itk34ConfidenceConnectedImageAsymFilterINS_5ImageItLj2EEENS1_IhLj2EEEE7GetMeanEv _ZN3itk23UnaryFunctorImageFilterINS_5ImageIfLj2EEES2_NS_7Functor4SqrtIffEEED0Ev _ZTIN3itk26ShapedNeighborhoodIteratorINS_5ImageImLj2EEENS_32ZeroFluxNeumannBoundaryConditionIS2_S2_EEE8IteratorE _ZNK3itk36VectorLinearInterpolateImageFunctionINS_5ImageINS_10FixedArrayIfLj2EEELj2EEEdE25EvaluateAtContinuousIndexERKNS_15ContinuousIndexIdLj2EEE _ZN3itk23ImageRegistrationMethodINS_5ImageItLj3EEES2_E9GetMetricEv _ZTIN3itk10RangeErrorE _ZN3itk12SmartPointerINS_24FiniteDifferenceFunctionINS_5ImageIdLj2EEEEEE10UnRegisterEv _Z21AntiAliasBinaryFilterItEvv _ZN7MLTypes14MLNumberStructIlEeqEe _ZN7MLTypes14MLNumberStructIcEgeEs _ZTSN3itk30SingleValuedNonLinearOptimizerE _ZNSt11__copy_moveILb0ELb0ESt26random_access_iterator_tagE8__copy_mIPKmPdEET0_T_S7_S6_ _ZN7MLTypes14MLNumberStructIeEdVEl _ZN3itk15CastImageFilterINS_5ImageImLj3EEENS1_IdLj3EEEE12GenerateDataEv _ZN3itk24ImageRegionConstIteratorINS_5ImageImLj2EEEED1Ev _ZNK3itk36GradientRecursiveGaussianImageFilterINS_5ImageIhLj3EEENS1_INS_15CovariantVectorIdLj3EEELj3EEEE13CreateAnotherEv _ZN3itk21NeighborhoodAllocatorIPfE10DeallocateEv _ZN3itk18ImageToImageFilterINS_5ImageImLj2EEENS1_INS_8RGBPixelIdEELj2EEEEC2Ev _ZTIN3itk9watershed11SegmentTreeIhEE _ZN3itk39RegularStepGradientDescentBaseOptimizer16StopOptimizationEv _ZTVN3itk12NeighborhoodINS_8RGBPixelIhEELj2ENS_21NeighborhoodAllocatorIS2_EEEE _ZNK3itk43FloodFilledImageFunctionConditionalIteratorINS_5ImageIhLj2EEENS_41MahalanobisDistanceThresholdImageFunctionINS1_INS_8RGBPixelItEELj2EEEfEEE3GetEv _ZNK3itk13ImageFunctionINS_5ImageINS_8RGBPixelItEELj3EEENS2_IdEEfE14GetNameOfClassEv _ZTIN3itk21ShiftScaleImageFilterINS_5ImageItLj2EEENS1_IdLj2EEEEE _ZN3itk33ImageRegionConstIteratorWithIndexINS_5ImageItLj3EEEEppEv _ZN3itk7Functor15BinaryThresholdIfmEC1Ev _ZTIPKN3itk5ImageINS_8RGBPixelItEELj2EEE _ZN6itksys9hashtableISt4pairIKmN3itk9watershed8BoundaryIdLj3EE13flat_region_tEEmNS_4hashImEENS_14hash_select1stIS2_S7_EESt8equal_toImESaIcEED2Ev _ZN3itk9watershed8BoundaryIfLj3EED1Ev _ZTSN3itk9OptimizerE _ZTSN3itk28GradientMagnitudeImageFilterINS_5ImageItLj2EEES2_EE _ZNK17double_conversion23DoubleToStringConverter31CreateExponentialRepresentationEPKciiPNS_13StringBuilderE _ZN7MLTypes14MLNumberStructIlEmLEx _ZN3itk31ConstShapedNeighborhoodIteratorINS_5ImageIhLj2EEENS_32ZeroFluxNeumannBoundaryConditionIS2_S2_EEE13ConstIteratorppEi _ZN3itk15CastImageFilterINS_5ImageImLj2EEENS1_ItLj2EEEED0Ev _ZNK3itk31AnisotropicDiffusionImageFilterINS_5ImageIhLj2EEES2_E9PrintSelfERSoNS_6IndentE _ZN3itk25ConstNeighborhoodIteratorINS_5ImageIhLj3EEENS_32ZeroFluxNeumannBoundaryConditionIS2_S2_EEED1Ev _ZN3itk27FiniteDifferenceImageFilterINS_5ImageIhLj2EEENS1_IdLj2EEEE25ManualReinitializationOffEv _ZNK3itk18ImageToImageFilterINS_5ImageIhLj2EEES2_E14GetNameOfClassEv _ZN3itk18ImageToImageFilterINS_5ImageIhLj3EEENS1_INS_15CovariantVectorIdLj3EEELj3EEEE14PushFrontInputEPKNS_10DataObjectE _ZN3itk13ObjectFactoryINS_25SimpleDataObjectDecoratorItEEE6CreateEv _ZTIN3itk13TransformBaseE _ZNK3itk27FiniteDifferenceImageFilterINS_5ImageINS_6VectorIfLj3EEELj2EEES4_E14GetNameOfClassEv _ZN3itk40AdaptiveHistogramEqualizationImageFilterINS_5ImageIfLj2EEEE16UseLookupTableOnEv _ZN3itk18ImageToImageFilterINS_5ImageINS_8RGBPixelIhEELj2EEENS1_IhLj2EEEED1Ev _ZN3itk25RegionalMinimaImageFilterINS_5ImageItLj2EEENS1_ImLj2EEEE17SetFullyConnectedEb _ZN7MLTypes14MLNumberStructIhEneEj _ZN3itk12SmartPointerINS_22ConstantPadImageFilterINS_5ImageIfLj2EEES3_EEE8RegisterEv _ZN3itk30LinearInterpolateImageFunctionINS_5ImageItLj2EEEdED1Ev _ZN3itk25ReconstructionImageFilterINS_5ImageItLj2EEES2_St4lessItEE12GenerateDataEv _ZN3itk18ImageToImageFilterINS_5ImageIhLj3EEENS1_IfLj3EEEE22VerifyInputInformationEv _ZN12vnl_c_vectorIlE3sumEPKlj _ZN9__gnu_cxx14__alloc_traitsISaIlEE8allocateERS1_j _ZNK3itk23UnaryFunctorImageFilterINS_5ImageIdLj2EEENS1_INS_8RGBPixelIdEELj2EEENS_7Functor4CastIdS4_EEE14GetNameOfClassEv _ZTSN3itk18ImageToImageFilterINS_5ImageIfLj2EEENS1_ItLj2EEEEE _ZTIN3itk27ImageConstIteratorWithIndexINS_5ImageIfLj3EEEEE _ZN3itk43FloodFilledFunctionConditionalConstIteratorINS_5ImageINS_8RGBPixelItEELj2EEENS_28BinaryThresholdImageFunctionINS1_IhLj2EEEfEEE18InitializeIteratorEv _ZNK10vnl_matrixImE5emptyEv _ZTIN3itk32ZeroFluxNeumannBoundaryConditionINS_5ImageIaLj2EEES2_EE _ZN3itk26ImageScanlineConstIteratorINS_5ImageImLj2EEEEC1EPKS2_RKNS_11ImageRegionILj2EEE _ZN3itk5ImageINS_15CovariantVectorIdLj3EEELj3EE17SetPixelContainerEPNS_20ImportImageContainerImS2_EE _ZN7MLTypes14MLNumberStructIiEgtEh _ZNK3itk18ImageToImageMetricINS_5ImageIdLj3EEES2_E40GetValueAndDerivativeThreadProcessSampleEjmRKNS_5PointIdLj3EEEdRKNS_15