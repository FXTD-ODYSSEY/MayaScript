# -*- coding: utf-8 -*-
"""
Hans Godard -- zapan669@hotmail.com
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-10 14:12:22'


import math
from maya import OpenMaya, OpenMayaMPx



class MatrixNN( object ):
	'''
	matrices de la forme  liste de lignes
	exemple  A = [[0,3,1],[2,1,0],[1,0,3]]
	'''
	
	def __init__(self):
		
		# dimension
		# row column values
		self.dim	= None
		self.rc	= None
	
	def setDimension( self, dim ):
		
		self.dim	= dim
		self.setIdentity()
	
	def setIdentity(self):
		self.rc	= [[float(i == j) for i in xrange(self.dim)] for j in xrange(self.dim)]
	
	def remove_rc(self, r, c):
		'''retire la ligne[ r ]   et la colonne[ c ]  dans toutes les lignes restantes
		et reduit la dim bien sur'''
		
		self.rc.pop( r )
		
		self.dim	-= 1
		
		for i in xrange(self.dim) :
			self.rc[ i ].pop( c )
		
	def reduceDim(self, m,n,M):
		'''retourne la matrice A sans la m ième ligne et la n ième colonne'''
		Mlin=len(M)
		result=[]
		red=[]
		for i in xrange(Mlin):
			if i!=m:
				for j in xrange(Mlin):
					if (j!=n):
						result.append(M[i][j])
		for k in xrange(0,len (result),Mlin-1):
			red.append(result[k:k+Mlin-1])
		return red
	
	def determinant(self, A):
		'''retourne le déterminat de la matrice A'''
		if len(A)==1:
			return A[0][0]
		if len(A)==2:
			r=A[0][0]*A[1][1]-A[0][1]*A[1][0]
			return r
		else:
			s=0
			j=0
			while j<len(A):
				B=self.reduceDim(j,0,A)
				if j%2==0:
					s=s+A[j][0]*self.determinant(B)
				else:
					s=s-A[j][0]*self.determinant(B)
				j=j+1
			return s
	
	def comat(self, A):
		'''Donne la comatrice d'une matrice A'''
		n=self.dim
		k=0
		com=[None]*n
		while k<n:
			com[k]=[0]*n
			l=0
			while l<n:
				B=self.reduceDim(k,l,A)
				if (k+l)%2==0:
					com[k][l]=(self.determinant(B))
				else:
					com[k][l]=((-1)*self.determinant(B))
				l=l+1
			k=k+1
		return com
	
	def transpos(self, A):
		'''Donne la transposée d'une matrice A'''
		n=self.dim
		M=[None]*n
		for i in xrange(n):
			M[i]=[0]*n
			for j in xrange(n):
				M[i][j]=A[j][i]
		return M
	
	def multCoef(self, A,r):
		'''Donne le produit d'une matrice A par le coefficient r'''
		n=self.dim
		Mat=[None]*n
		for i in xrange(n):
			Mat[i]=[0]*n
			for j in xrange(n):
				Mat[i][j]=r*A[i][j]
		return Mat
	
	def inverse(self, A):
		'''renvoi l'inverse d'une matrice carrée'''
		d=self.determinant(A)
		if d==0:
			return 'La Matrice n\'est pas inversible'
		else:
			B=self.multCoef(self.comat(A),1./d)
			inv=self.transpos(B)
		return inv
	
	
	def mult(self, A, B):
		'''renvoi le produit des 2 '''
		TB = zip(*B)
		return [ [ sum(ea*eb for ea,eb in zip(a,b))  for b in TB ] for a in A ]
	
	def factorize_LU( self ):
		'''decomposition   A = LU   L lower triangular matrix   et   U upper triangular
		renvoi aussi les ids de Permutation'''
		
		# LU est une initialement une copie de self
		LU	= list( self.rc )
		
		
		nRows, nCols	= self.dim, self.dim
		if nRows <= 1 :
			return None, None
		
		
		# Permutation Indices
		Pids		= range(self.dim)
		
		
		
		# deja trouve les plus gros par ligne :
		s	= [.0]*nRows
		
		for i in xrange( nRows ):
			smax		= .0
			for j in xrange( nRows ):
				smax	= max(  smax, abs(LU[i][j]) )
			s[i]		= smax
		
		
		
		
		for k in xrange(nRows-1):
			
			# Find the remaining row with the largest scaled pivot.
			#colMax	= LU[k][k]
			Pid		= k
			rmax		= .0
			
			for i in xrange( k, nRows ):
				
				r	= abs(LU[Pids[i]][k] / s[Pids[i]])
				
				if r > rmax :
					rmax	= r
					j = i
			# Row j has the largest scaled pivot, so "swap" that row with the
			# current row (row k).  The swap is not actually done by copying rows,
			# but by swaping two entries in an index vector.
			
			Pids[j], Pids[k]	= Pids[k], Pids[j]
			
			# Now carry out the next elimination step as usual, except for the
			# added complication of the index vector.
			for i in xrange(k+1, nRows):
				xmult	= LU[Pids[i]][k] / LU[Pids[k]][k]
				LU[Pids[i]][k] = xmult
				
				for j in xrange(k+1,  nCols):
					LU[Pids[i]][j] = LU[Pids[i]][j] - xmult*LU[Pids[k]][j]
				
		
		return LU, Pids
	
	def solve_LU( self, LU, Pids, b ):
		'''Solve LUx= b '''
		
		
		nRows, nCols	= self.dim, self.dim
		x	= [.0]*nRows
		
		
		for k in xrange( nRows-1):
			for i in xrange( k+1, nRows):
				b[Pids[i]] = b[Pids[i]] - LU[Pids[i]][k] * b[Pids[k]]
		
		for i in xrange( nRows-1, -1,-1):
			sum_ = b[Pids[i]]
			for j in xrange( i+1, nRows):
				sum_ = sum_ - LU[Pids[i]][j] * x[j]
			x[i] = sum_ / LU[Pids[i]][i]
		
		return x
	
	



class RbfSolver(OpenMayaMPx.MPxNode):
	
	kPluginNodeName	= "rbfSolver"
	kPluginNodeId		= OpenMaya.MTypeId(0x0B8D357)
	
	epsilon	= 10e-15
	
	
	
	def euclidian_distance( dim, vec1, vec2 ):
		
		subVector	= [ vec1[n]-vec2[n]	for n in xrange(dim) ]
		
		powi_sum	= sum( pow( abs(subVector[i]), dim ) for i in xrange(dim)  )
		
		return pow( powi_sum, 1.0/dim )
	
	
	def angular_distance(  dim, vec1, vec2 ):
		'''les vectors doivent etre normalisés  et de dimension 3 maximum'''
		
		dot	= sum( vec1[n]*vec2[n]	for n in xrange(dim)    )
		if dot>1.0:	dot=1.0
		elif dot<-1.0:	dot=-1.0
		
		angle_rad	= math.acos(dot)
		
		return angle_rad
	
	# pour une angular distance  la dimensionN ne peut pas dépasser 3
	# et les vectors doivent etre normalisés
	# Quelque soit la fonction,  fScale est multiplié par la distance
	distance_fonctions	= (	euclidian_distance,
						angular_distance,  )
	
	
	def set_range( self, x, x0, x1, y0, y1 ) :
		y   = 1.0*(  y0 + (x-x0)*(y1-y0)/(x1-x0)  )
		return y
	
	
	def linear_RBF( d ):
		return d
		
	def gaussian_RBF( d ):
		return math.exp( - d*d )
		
	def multiquadric( d ):
		return math.sqrt( 1.0+d*d  )
		
	def inverseQuadratic_RBF( d ):
		return 1.0/(1.0+d*d )
		
	def inverseMultiquadratic_RBF( d  ):
		return 1.0/math.sqrt(  (1.0+d*d )  )
		
	def cubic_RBF( d ):
		return d*d*d +1.0
		
	def thinPlate_RBF( d ):
		# pas définie en 0 donc utilise un epsilon
		if d<RbfSolver.epsilon:
			d=RbfSolver.epsilon
		return  d*d*math.log(d)
	
	# fonction +  variationId
	# variationId = 0	--->  décroissante	sur  ]0,+infini[
	# variationId = 1	--->  croissante		sur  ]0,+infini[
	rbf_fonctions	= (	linear_RBF,
					gaussian_RBF,
					multiquadric,
					inverseQuadratic_RBF,
					inverseMultiquadratic_RBF,
					cubic_RBF,
					thinPlate_RBF,  )
	
	
	
	
	@classmethod
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )
	
	@classmethod
	def nodeInitializer( cls ):
		numAttr	= OpenMaya.MFnNumericAttribute()
		compAttr	= OpenMaya.MFnCompoundAttribute()
		enumAttr	= OpenMaya.MFnEnumAttribute()
		
		
		cls.NDimension		= numAttr.create( "NDimension","nd",OpenMaya.MFnNumericData.kInt, 1 )
		numAttr.setMin(1)
		cls.MDimension	= numAttr.create( "MDimension","md",OpenMaya.MFnNumericData.kInt, 1 )
		numAttr.setMin(1)
		
		cls.distanceMode	= enumAttr.create( "distanceMode","dist",  0 )
		enumAttr.addField( "Euclidian" , 0 )
		enumAttr.addField( "Angular" , 1 )
		
		cls.rbfMode	= enumAttr.create( "rbfMode","rbf",  1)
		enumAttr.addField( "Linear" , 0 )
		enumAttr.addField( "Gaussian" , 1 )
		enumAttr.addField( "Multiquadratic" , 2 )
		enumAttr.addField( "Inverse Quadratic" , 3 )
		enumAttr.addField( "Inverse Multiquadratic" , 4 )
		enumAttr.addField( "Cubic" , 5 )
		#enumAttr.addField( "Thin Plate " , 6 )
		
		# Scale est multiplié par la distance
		cls.scale		= numAttr.create( "scale","sc",OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setMin(cls.epsilon)
		
		cls.normalize	= numAttr.create( "normalize","nz", OpenMaya.MFnNumericData.kBoolean, True)
		
		# force output in 0-1 range
		cls.blendShapeMode  = numAttr.create("blendShapeMode", "bsm", OpenMaya.MFnNumericData.kBoolean, False)
		
		
		cls.nInput	= numAttr.create( "nInput","ni",OpenMaya.MFnNumericData.kFloat, .0)
		numAttr.setKeyable(True)
		numAttr.setArray(True)
		
		# poses
		# N = inDim	= dim( nInput )	= dim( keys )
		# M = outDim	= dim( mOutput )= dim( values )
		cls.state	= numAttr.create( "state","st",OpenMaya.MFnNumericData.kBoolean, True)
		#cls.weight	= numAttr.create( "weight","w",OpenMaya.MFnNumericData.kFloat, 1.0)
		cls.nKey	= numAttr.create( "nKey","nk",OpenMaya.MFnNumericData.kFloat, .0)
		numAttr.setArray(True)
		cls.mValue	= numAttr.create( "mValue","mv",OpenMaya.MFnNumericData.kFloat, .0)
		numAttr.setArray(True)
		
		cls.poses	= compAttr.create( "poses" , "ps")
		compAttr.addChild( cls.state )
		#compAttr.addChild( cls.weight )
		compAttr.addChild( cls.nKey )
		compAttr.addChild( cls.mValue )
		compAttr.setArray(True)
		
		
		# out
		cls.solved		= numAttr.create( "solved", "sv", OpenMaya.MFnNumericData.kBoolean, True)
		numAttr.setHidden( True )
		
		cls.mOutput	= numAttr.create( "mOutput","mo",OpenMaya.MFnNumericData.kFloat, .0)
		numAttr.setWritable( False )
		numAttr.setArray(True)
		numAttr.setUsesArrayDataBuilder( True)
		
		
		
		# add 
		for attr in (	cls.NDimension,
					cls.MDimension,
					cls.scale,
					cls.normalize,
					cls.blendShapeMode,
					cls.solved,
					cls.nInput,
					cls.distanceMode,
					cls.poses,
					cls.rbfMode,
					cls.mOutput,  ):
			cls.addAttribute( attr )
		
		
		# tout SAUF nInput regenere le system
		for attr in (	cls.NDimension,
					cls.MDimension,
					cls.distanceMode,
					cls.rbfMode,
					cls.scale,
					cls.normalize,
					#cls.solved,
					cls.poses,
					):
			cls.attributeAffects(  attr, cls.solved )
		
		
		# tout recalcul les outputs 
		for attr in (	cls.NDimension,
					cls.MDimension,
					cls.distanceMode,
					cls.rbfMode,
					cls.scale,
					cls.normalize,
					cls.blendShapeMode,
					cls.solved,
					cls.poses,
					cls.nInput,	# 	<<<<<---------------
					):
			cls.attributeAffects( attr, cls.mOutput )
		
		
		# AE reorder
		cls.init_AETemplate()
	
	
	@classmethod
	def init_AETemplate( cls  ):
		AE_cmd = '''
		global proc AE[nodeType]Template( string $nodeName )
		{
		editorTemplate -beginScrollLayout;
			editorTemplate -beginLayout "Main Attributes" -collapse 0;
				editorTemplate -addControl "NDimension";
				editorTemplate -addControl  "MDimension" ;
				editorTemplate -addSeparator ;
				editorTemplate -addControl "distanceMode";
				editorTemplate -addControl "rbfMode";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "scale";
				editorTemplate -addControl "normalize";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "blendShapeMode";
				editorTemplate -addControl "nInput";
				editorTemplate -addControl "poses";
			editorTemplate -endLayout;
			editorTemplate -addExtraControls;
		editorTemplate -endScrollLayout;
		}
		'''.replace("[nodeType]", cls.kPluginNodeName )
		OpenMaya.MGlobal.executeCommand( AE_cmd )
	
	
	@classmethod
	def isPassiveOutput(self, plug):
		return True
	
	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		
		
		# infos de base interrogées dans le rebuild_solver
		# inutil de les ré-interroger a chaque fois
		self.N		= 1
		self.M		= 1
		self.fScale	= 1.0
		
		
		# infos calculées dans le rebuild_solver
		self.distance_fonction	= None
		self.rbf_fonction		= None
		
		self.poseUsed_ids	= []
		
		
		# évite les dico pour le framerate !!
		# nVector	par pose   contenant les poses clés
		# weight	par pose
		self.nKeys		= []
		self.weights	= []
		
		# mVector contenant les coefficient solved
		self.mX		= []
		
		
		# in the case of only one pose, there is no interpolation so store the mValue and return it in the .compute()
		self.only_one_mValue    = []
	
	
	
	
	def rebuild_solver( self, data ):
		'''recalcule le solver a l'aide de matrixMM 
		aucun  input ou output dans ce code '''
		
		
		self.N	= data.inputValue( self.NDimension ).asInt()
		self.M	= data.inputValue( self.MDimension ).asInt()
		
		poses_H		= data.inputArrayValue( self.poses )
		pose_ids		= OpenMaya.MIntArray()
		OpenMaya.MPlug( self.thisMObject(), self.poses).getExistingArrayAttributeIndices( pose_ids )
		
		self.poseUsed_ids	    = [] #   = pose_ids  utilisées
		
		# trouve les infos necessaires pour creer le system
		self.nKeys		= [] # liste (dim  poses_num) 	de liste ( dim N )
		mValues		    = [] # liste (dim  poses_num) 	de liste ( dim M )
		self.weights	= [] # liste (dim  poses_num) 	de floats
		self.only_one_mValue    = []
		
		
		for i in pose_ids :
			
			poses_H.jumpToElement( i )
			pose_H	= poses_H.inputValue()
			
			state		= pose_H.child( self.state ).asBool()
			#wgt		= pose_H.child( self.weight ).asFloat()
			
			#if not (state and wgt>self.epsilon)  :
			#	continue
			if not state :
				continue
			
			
			nKey_H	    = OpenMaya.MArrayDataHandle( pose_H.child( self.nKey ) )
			nKey		= []
			mValue_H	= OpenMaya.MArrayDataHandle( pose_H.child( self.mValue ) )
			mValue	    = []
			
			
			for n in xrange(self.N):
				# try au cas ou y'aurai rien de branché ...
				try :
					nKey_H.jumpToElement( n )
					key		= nKey_H.inputValue().asFloat()
					nKey.append( key )
				except :
					nKey.append( .0 )
			
			
			
			# ignore les clé deja presentes
			if nKey in self.nKeys :
				OpenMaya.MGlobal.displayWarning( 'key[%s] %s  can not be used more than once' %(i,nKey) )
				continue
			
			
			#
			for m in xrange(self.M):
				try:
					mValue_H.jumpToElement( m )
					value		= mValue_H.inputValue().asFloat()
					mValue.append( value )
				except: 
					mValue.append( .0 )
			
			
			#
			self.nKeys.append( nKey )
			mValues.append( mValue )
			#self.weights.append( wgt )
			
			self.poseUsed_ids.append( i )
		
		
		
		#
		poseUsed_num    = len(self.poseUsed_ids)
		
		if poseUsed_num == 0 :
			OpenMaya.MGlobal.displayError( 'RbfSolver failed : No Key' )
			return False
		
		elif poseUsed_num==1 :
			# no interpolation
			self.only_one_mValue  = mValues[0]
			return True
		
		
		
		
		
		# pour la suite necessite de connaitre les fonctions utilisées :
		# Distance fonction ?
		# RBF fonction ?
		normalize		= data.inputValue( self.normalize ).asBool()
		
		distance_id		= data.inputValue( self.distanceMode ).asInt()
		self.distance_fonction	= self.distance_fonctions[ distance_id ]
		
		rbf_id			= data.inputValue( self.rbfMode).asInt()
		self.rbf_fonction	= self.rbf_fonctions[ rbf_id ]
		
		
		
		
		# matrixMM pour resoudre les system AX = Y
		# factorize la   et    solve la pour chaque m
		# store les X(m)   dans   self.mX
		distanceMax	= .0
		
		mat		= MatrixNN()
		mat.setDimension( poseUsed_num )
		
		
		
		#** pour les poses doublon
		# remove les  [ligne-colonne]  contenant .0 en dehor de la diagonale
		
		for i in xrange(poseUsed_num) :
			for j in xrange(poseUsed_num) :
				
				if i==j :
					# ici la distance d'une pose sur elle meme
					mat.rc[i][j]	= .0
				else :
					# distance de chaque pose a chaque pose
					distance	= self.distance_fonction( self.N, self.nKeys[ i ], self.nKeys[ j ]  )
					
					# stock la distance maximale entre 2 poses
					# ceci servira à la normalisation du system
					if distance > distanceMax :
						distanceMax = distance
					
					
					mat.rc[i][j]	= distance
		
		
		
		
		# utilise le scale pour smoother plus ou moins
		# si on veut le system normalisé, il faut disiviser le scale par la distanceMax
		fScale	= data.inputValue( self.scale ).asFloat()
		if fScale < self.epsilon :
			fScale = self.epsilon
		
		
		if normalize :
			self.fScale	= fScale	/ distanceMax
		else :
			self.fScale	= fScale
		
		
		# RBF chaque element
		for i in xrange(poseUsed_num) :
			for j in xrange(poseUsed_num) :
				
				# euclidienne ou angulaire ?  ou autre...
				mat.rc[i][j]	= self.rbf_fonction( mat.rc[i][j] * self.fScale )
			
		
		
		
		
		# factorizeLU  et sauve les ids des lignes permutées
		LU, Pids	= mat.factorize_LU()
		
		
		
		
		# pour chaque m de chaque pose
		# solv_LU  et store les X(m)   dans   self.mX
		# mX =  m * nVector
		self.mX	= []
		
		for m in xrange(self.M):
			
			Y	= [ mValues[ i ][ m ]  for i in xrange(poseUsed_num) ]
			
			X	= mat.solve_LU(  LU, Pids, Y )	# nVector des coeff
			
			self.mX.append( X )
		
		
		
		
		#*** setClean  indique que le system  est  solved
		solved_H	= data.outputValue( self.solved )
		solved_H.setClean()
		
		OpenMaya.MGlobal.displayInfo( "RbfSolver recomputed using poses :  %s" %self.poseUsed_ids )
		return True
	
	
	
	
	
	def compute(self, plug, data):
		
		
		if not plug==self.mOutput:
			return
		
		#***
		if not data.isClean( self.solved ):
			status	= self.rebuild_solver( data )
			
			if not status :
				return
		
		
		
		
		# trouve le nVector nInput
		nInput_H	= data.inputArrayValue( self.nInput )
		nInput		= []
		
		for n in xrange(self.N):
			try :
				nInput_H.jumpToElement( n )
				input_	= nInput_H.inputValue().asFloat()
				nInput.append( input_ )
			except :
				nInput.append( .0 )
		
		
		
		
		# il suffit d'appliquer  Somme des  Xi * ||p-Di||  pour chaque m
		output_Handle	= data.outputArrayValue( self.mOutput )
		poseUsed_num	= len(self.poseUsed_ids)
		
		if poseUsed_num==1:
			# no interpolation, set the mValue directly
			self.set_mOutput( self.only_one_mValue, output_Handle )
			
			output_Handle.setAllClean()
			data.setClean( plug )
			return
		
		
		# else
		outputs         = [.0]*self.M
		
		for m in xrange(self.M):
			for i in xrange(poseUsed_num):
				
				# calcul la distance
				# applique pose weight
				# applique RBF
				# applique coeff Xi
				distance	= self.distance_fonction( self.N, nInput, self.nKeys[ i ]  )
				distance	= self.rbf_fonction( distance * self.fScale  )
				distance	= self.mX[m][i] * distance
				outputs[m]  +=  distance
		
		
		
		#
		blendShapeMode  = data.inputValue(self.blendShapeMode).asBool()
		
		if blendShapeMode==True :
			
			min     = None 
			for m in xrange(self.M):
				if (m==0) or (outputs[m] < min):
					min     = outputs[m]
			
			sum     = .0
			for m in xrange(self.M):
				outputs[m]  = self.set_range( outputs[m], min, 1.0, .0, 1.0 )
				sum        += outputs[m]
			
			for m in xrange(self.M):
				outputs[m]  /= sum
			
			
		#
		self.set_mOutput( outputs, output_Handle )
		output_Handle.setAllClean()
		data.setClean( plug )
	
	
	
	def set_mOutput(self, outputs, output_Handle):
		
		for m in xrange(self.M):
			try :
				output_Handle.jumpToElement( m )
				output_Handle.outputValue().setFloat( outputs[m] )
			except :
				pass
			
			
		
		
	
	
		
	

def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard -- zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode( RbfSolver.kPluginNodeName, RbfSolver.kPluginNodeId, RbfSolver.nodeCreator, RbfSolver.nodeInitializer )
	except:
		OpenMaya.MGlobal.displayError( "Failed to register node: %s\n" % RbfSolver.kPluginNodeName )
		raise

def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( RbfSolver.kPluginNodeId )
	except:
		OpenMaya.MGlobal.displayError( "Failed to unregister node: %s\n" % RbfSolver.kPluginNodeName )
		raise
