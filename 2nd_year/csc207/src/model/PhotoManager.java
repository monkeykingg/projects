package model;

import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Date;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;
import javafx.util.Pair;

import auxiliary.CannotUndoNameException;
import auxiliary.DuplicateTagException;
import auxiliary.FailToRenamePhotoFileException;
import auxiliary.FileTypeException;
import auxiliary.NotAnExistingTagException;

/**
 * A photo manager based on a root, which organizes all File, specifically
 * directories and photos, and their corresponding FileNode or PhotoNode in the
 * hierarchy.
 */
public class PhotoManager extends FileManager {

	/** A Logger for PhotoManager. */
	private static final Logger logger = Logger.getLogger(PhotoNode.class.getName());

	/** A FileHandler for PhotoManager. */
	private static FileHandler fileHandler;

	/**
	 * The tree rooted at the root file of the PhotoManager, represented by a
	 * FileNode and its hierarchy (but only maintaining directories and photos).
	 * If the PhotoManager is based on a single photo, then it is actually a
	 * photoNode.
	 */
	private FileNode photoTree;

	/**
	 * The list keeping track of all 2-element pairs for (File photo,
	 * corresponding PhotoNode) in the PhotoManager, regardless of the hierarchy
	 * in the directory system.
	 */
	private ArrayList<Pair<File, PhotoNode>> flattenedPhotoCollection;

	/**
	 * A set of existing tags, which is the collection of all tags tagged to
	 * some photo in this photo management system.
	 */
	private TagManager existingTags;

	/**
	 * A photo manager.
	 *
	 * @param root
	 *            the File root on which the file manager is based (which can be
	 *            a photo, or a directory)
	 * @param rootNode
	 *            the FileNode representing the root
	 * @throws FileTypeException
	 */
	public PhotoManager(File root, FileNode rootNode) throws FileTypeException {
		// PhotoManager has a FileManager part. Call super's constructor.
		super(root, rootNode);

		// Check type of the root, instantiate instance variables photoTree and
		// flattenedPhotoCollection if the root is a directory or a photo,
		// otherwise throw an exception.
		if (root.isDirectory()) {

			photoTree = new FileNode(root.getName(), null, FileType.DIRECTORY);
			buildPhotoTree(root, photoTree);
			flattenedPhotoCollection = flattenPhoto(root, photoTree);
		} else if (rootNode.isPhoto()) {

			photoTree = new PhotoNode(rootNode.getName(), rootNode.getParent());
			flattenedPhotoCollection = new ArrayList<Pair<File, PhotoNode>>();
			flattenedPhotoCollection.add(new Pair<File, PhotoNode>(root, (PhotoNode) photoTree));
		} else {

			String msg = root.getName()
					+ " is neither a directory nor a photo, can't construct a PhotoManager on that!";
			throw new FileTypeException(msg);
		}

		// Do the configuration.
		// existingTags will be initialized in this process.
		try {
			config(root);
		} catch (ClassNotFoundException | IOException e1) {
			e1.printStackTrace();
		}
	}

	/**
	 * Return the tree rooted at the root file of the PhotoManager, represented
	 * by a FileNode and its hierarchy (but only maintaining directories and
	 * photos). If the PhotoManager is based on a single photo, then it is
	 * actually a photoNode.
	 * 
	 * @return the photoTree
	 */
	public FileNode getPhotoTree() {
		return photoTree;
	}

	/**
	 * Return the list keeping track of all 2-element pairs for (File photo,
	 * corresponding PhotoNode) in the PhotoManager, regardless of the hierarchy
	 * in the directory system.
	 * 
	 * @return the flattenedPhotoCollection
	 */
	public ArrayList<Pair<File, PhotoNode>> getFlattenedPhotoCollection() {
		return flattenedPhotoCollection;
	}

	/**
	 * Return a set of existing tags, which is the collection of all tags tagged
	 * to some photo in this photo management system.
	 * 
	 * @return the existingTags
	 */
	public TagManager getExistingTags() {
		return existingTags;
	}

	/**
	 * Set existingTags to a new TagManager newExistingTags.
	 * 
	 * @param newExistingTags
	 *            the new TagManager to set
	 */
	public void setExistingTags(TagManager newExistingTags) {
		this.existingTags = newExistingTags;
	}

	/**
	 * Build the tree of nodes rooted at file in the file system and curr is the
	 * FileNode corresponding to file. This only adds nodes for photo or
	 * directory as children of file to the tree. Precondition: file represents
	 * a directory.
	 * 
	 * @param file
	 *            the directory we are building
	 * @param curr
	 *            the node representing file
	 */
	public void buildPhotoTree(File file, FileNode curr) {
		// file always represents a directory; deal with items
		// inside the directory if here's any
		File[] contents = file.listFiles();
		for (File item : contents) {
			FileNode child = null;
			if (item.isDirectory()) {

				// If item is a directory, instantiate a FileNode corresponding
				// to item, add that to curr's children, and recursively build
				// the tree of nodes.
				child = new FileNode(item.getName(), curr, FileType.DIRECTORY);
				curr.addChild(child.getName(), child);
				buildPhotoTree(item, child);
			} else {

				// If child is a non-image file, instantiate a FileNode, but we
				// don't bother add it as a child.
				BufferedImage img = null;
				try {
					img = ImageIO.read(item);
				} catch (IOException e) {
					child = new FileNode(item.getName(), curr, FileType.FILE);
				}

				// If child is a photo, instantiate a PhotoNode.
				if (img != null) {
					child = new PhotoNode(item.getName(), curr);

					// Add the PhotoNode corresponding to item as a child of
					// curr
					curr.addChild(child.getName(), child);
				}
			}
		}
	}

	/**
	 * Return a list keeping track of all 2-element pairs for (File photo,
	 * corresponding PhotoNode) in the directory tree rooted at file, regardless
	 * of the hierarchy in the directory system. Precondition: file and fileNode
	 * represents a directory.
	 * 
	 * @param file
	 *            the directory to get all 2-element pairs for (File photo,
	 *            corresponding PhotoNode) for photos inside that directory
	 * @param fileNode
	 *            the corresponding node representing the directory to get the
	 *            flattened photo collection
	 * @return a list keeping track of all 2-element pairs for (File photo,
	 *         corresponding PhotoNode) in the directory tree rooted at file,
	 *         regardless of the hierarchy in the directory system
	 */
	public ArrayList<Pair<File, PhotoNode>> flattenPhoto(File file, FileNode fileNode) {
		// Construct an accumulator.
		ArrayList<Pair<File, PhotoNode>> acc = new ArrayList<Pair<File, PhotoNode>>();

		// Due to precondition, file and fileNode represent the same directory.
		// We can handle the children of that directory.
		for (FileNode childNode : fileNode.getChildren()) {

			// Match childFile with childNode
			File childFile = null;
			for (File f : file.listFiles()) {
				if (f.getName().equals(childNode.getName())) {
					childFile = f;
				}
			}
			if (childFile.isDirectory()) {

				// If childFile is a directory, we collect all photos in the
				// directory and its hierarchy if here's any.
				acc.addAll(flattenPhoto(childFile, childNode));
			} else if (childNode.isPhoto()) {

				// If childNode is a PhotoNode, add that and its
				// corresponding file to the accumulator.
				acc.add(new Pair<File, PhotoNode>(childFile, (PhotoNode) childNode));
			}

			// If fileNode is a non-image file, we don't bother to do anything.
		}

		return acc;
	}

	/**
	 * Do the configuration for a photoManager based on File file. If there were
	 * any configuration files already existed, directly import them; otherwise
	 * make new plain configuration files for further use.
	 *
	 * @param file
	 *            the root file on which this photoManager is based
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public void config(File file) throws IOException, ClassNotFoundException {
		// Check the type of file and handle different kinds of files
		if (file.isDirectory()) {

			// If file is a directory, check whether there's already
			// configuration files in it; if here's any, directly import and use
			// them, otherwise create new configuration files.
			String dirPath = file.getAbsolutePath();
			configDir(dirPath);

		} else {

			// If file is a photo, check configuration files in the directory
			// containing it if; if here's any, directly import and use them,
			// otherwise create new configuration files.
			// If file is a non-image file, throw an exception.
			BufferedImage img = null;

			try {
				img = ImageIO.read(file);

			} catch (IOException e) {
				e.printStackTrace();
			}

			if (img != null) {
				String dirPath = file.getParentFile().getAbsolutePath();
				configDir(dirPath);
			}
		}
	}

	/**
	 * Do the configuration for a specified directory which has the absolute
	 * path dirPath.
	 * 
	 * @param dirPath
	 *            the absolute path of the directory for which the configuration
	 *            need to be done
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	private void configDir(String dirPath) throws FileNotFoundException, IOException, ClassNotFoundException {
		// Configure the TagManager
		String tagPath = dirPath + File.separator + "Tags.ser";
		configTagManager(tagPath);

		// Configure the log file
		String logPath = dirPath + File.separator + "Log.txt";
		configLog(logPath);
	}

	/**
	 * Configure a TagManager in the specified path. If the configuration file
	 * already exists in the specified path, import the object in the
	 * configuration file. Otherwise, create a configuration file for
	 * TagManager.
	 * 
	 * @param path
	 *            the specified path to configure the TagManager
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	private void configTagManager(String path) throws FileNotFoundException, IOException, ClassNotFoundException {
		File f = new File(path);

		// If the configuration file exists already, read that.
		// If there's no existing configuration file, create one.
		if (f.exists()) {

			existingTags = readTagManager(path);
		} else {

			// Extract all existing tags based on all photos in this
			// PhotoManager and construct a TagManger, then write that
			// TagManager object into the plain configuration file specified at
			// path.
			existingTags = contructTagManager(flattenedPhotoCollection);
			writeTagManger(existingTags, path);
		}
	}

	/**
	 * Return a TagManager object read from a specified path if the path is
	 * valid.
	 * 
	 * @param path
	 *            the path to read TagManager object
	 * @return the TagManager object stored in the specified path
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public TagManager readTagManager(String path) throws FileNotFoundException, IOException, ClassNotFoundException {
		// Read object
		InputStream inputStream = new FileInputStream(path);
		InputStream buffer = new BufferedInputStream(inputStream);
		ObjectInput input = new ObjectInputStream(buffer);
		TagManager tagManager = (TagManager) input.readObject();

		// Close the stream
		input.close();

		return tagManager;
	}

	/**
	 * Return a well-constructed TagManager based on a collection of photo files
	 * and their corresponding nodes.
	 * 
	 * @param flattenedPhotos
	 *            a collection of all photos files and their corresponding
	 *            PhotoNode
	 * @return a TagManager based on all photos collected in the flattenedPhotos
	 */
	public TagManager contructTagManager(ArrayList<Pair<File, PhotoNode>> flattenedPhotos) {
		// Construct an accumulator.
		TagManager tagManager = new TagManager();

		// Loop over all pairs in flattenedPhotos to collect all tags.
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {
			ArrayList<Tag> tags = photoPair.getValue().getCurrPhotoName().getLstPhotoTags();
			for (Tag t : tags) {
				tagManager.addTag(t);
			}
		}
		return tagManager;
	}

	/**
	 * Write a TagManager object tagManager to the file at the specified path.
	 * 
	 * @param path
	 *            the path to write TagManager object tagManager
	 * @param tagManager
	 *            the TagManager to write
	 * @throws IOException
	 */
	public void writeTagManger(TagManager tagManager, String path) throws IOException {
		// Write object
		OutputStream file = new FileOutputStream(path, false);
		OutputStream buffer = new BufferedOutputStream(file);
		ObjectOutput output = new ObjectOutputStream(buffer);
		output.writeObject(tagManager);

		// Close stream
		output.close();
	}

	/**
	 * Configure log file at a specified path logPath. If there's already a
	 * configuration file existing, leave the file there for further usage of
	 * logging. Otherwise, create a new file to store logging info.
	 * 
	 * @param logPath
	 *            the path to configure log file
	 * @throws IOException
	 */
	private void configLog(String logPath) throws IOException {
		File log = new File(logPath);

		// Check the existence of configuration file for log.
		// If no existing configuration file, create a new one.
		if (!log.exists()) {
			log.createNewFile();
		}

		// Set up logging
		setUpLogging(logPath);
	}

	/**
	 * Set up logger and handler for PhotoManager.
	 * 
	 * @param path
	 *            the specified absolute path to put the log file
	 */
	private void setUpLogging(String path) {
		// Set up logger.
		logger.setLevel(Level.ALL);

		// Associate handler with logger.
		try {
			if (fileHandler == null) {
				fileHandler = new FileHandler(path, true);
				fileHandler.setFormatter(new SimpleFormatter());
				fileHandler.setLevel(Level.ALL);
				logger.addHandler(fileHandler);
			}
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Return the photo File after renaming. If the renaming failed, return the
	 * original File.
	 * 
	 * @param photo
	 *            the photo File to rename
	 * @param renamedPhotoNode
	 *            the corresponding photoNode whose name is already renamed
	 * @return the photo File after renaming
	 */
	private File renamePhotoFile(File photo, PhotoNode renamedPhotoNode) {
		// Keep track of the name before renaming
		String nameBefore = photo.getName();

		// Rename by specifying a new path.
		String absPath = photo.getAbsolutePath();
		int lastSeparator = absPath.lastIndexOf(File.separator);
		String newPath = absPath.substring(0, lastSeparator + 1) + renamedPhotoNode.getName();
		File newPhoto = new File(newPath);

		// Record whether the renaming succeeded or not and return corresponding
		// File result.
		String msg;
		if (photo.renameTo(newPhoto)) {

			msg = "Renaming succeeded: rename from " + nameBefore + " to " + renamedPhotoNode.getName();
			logger.log(Level.FINE, msg);
			return newPhoto;
		} else {

			// If the renaming failed, make the renamedPhotoNode go back to its
			// previous name.
			try {
				renamedPhotoNode.undoPhotoName();
			} catch (CannotUndoNameException e) {
				e.printStackTrace();
			}

			msg = "Renaming failed: name remained as before: " + nameBefore;
			logger.log(Level.INFO, msg);
			return photo;
		}
	}

	/**
	 * Revert the name of a photo back to a specified oldName and record that in
	 * the log if oldName is an existing past name for the photo. If there were
	 * several oldName existing as past names, revert to the latest one.
	 * 
	 * @param photo
	 *            the photo File to revert the name back to a specified oldName
	 * @param photoNode
	 *            the corresponding photo node to revert the name back to a
	 *            specified oldName
	 * @param oldName
	 *            the specified oldName to revert back to if it is an existing
	 *            past name
	 * @throws FailToRenamePhotoFileException
	 */
	public void logRevertName(File photo, PhotoNode photoNode, PhotoName oldName)
			throws FailToRenamePhotoFileException {
		// Keep track of the name before reverting.
		String nameBefore = photo.getName();

		// Revert name to the specified oldName both for the file and the
		// corresponding node if possible, otherwise record the occurrence of
		// exception in the log.
		try {
			ArrayList<Tag> originalTags = photoNode.getCurrPhotoName().getLstPhotoTags();
			photoNode.backToOlderName(oldName);

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is actually done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				ArrayList<Tag> newTags = photoNode.getCurrPhotoName().getLstPhotoTags();
				updateTagManager(originalTags, newTags);
			} else {

				// Log the failure of renaming the File name and throw an
				// exception
				String msg = "Reverting name failed: cannot rename the photo, " + photo.getName() + ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}
		} catch (CannotUndoNameException e) {

			// Record the exception in log and don't execute further steps.
			String msg = "Reverting name failed: cannot revert photo name from " + photo.getName() + " to "
					+ oldName.getStrPhotoName() + ", since the latter is not an existing past name for the photo";
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the reverting of the name if no exception was thrown.
		String logInfo1 = "Revert the name of a photo to its older name in a directory named: "
				+ photo.getParentFile().getName() + ":\n";
		String logInfo2 = "Name before reverting: " + nameBefore + "\n";
		String logInfo3 = "Name after reverting: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Revert the name of the photo back to the closest state merely before a
	 * particular time date if there were past names existed before that date
	 * for the photo. If the first name for the photo was generated after that
	 * date, revert back to the first name of the photo.
	 * 
	 * @param photo
	 *            the photo File to revert the name back to
	 * @param photoNode
	 *            the corresponding photo node to revert the name back to
	 * @param date
	 *            the time to revert back to
	 */
	public void logRevertNameByDate(File photo, PhotoNode photoNode, Date date) {
		// Keep track of the name before reverting.
		String nameBefore = photo.getName();

		// Revert name to the specified date both for the file and the
		// corresponding node.
		ArrayList<Tag> originalTags = new ArrayList<Tag>();
		for (Tag t : photoNode.getCurrPhotoName().getLstPhotoTags()) {
			originalTags.add(t);
		}
		photoNode.backToDate(date);

		// Keep track of the file we get after "renaming" to see whether the
		// renaming is actually done or not
		File renamedPhotoFile = renamePhotoFile(photo, photoNode);

		// Update the collection of photos, since File is immutable.
		updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

		// Update TagManager.
		ArrayList<Tag> newTags = photoNode.getCurrPhotoName().getLstPhotoTags();
		updateTagManager(originalTags, newTags);

		// Log the reverting of the name.
		String logInfo1 = "Revert the name of a photo back to the state merely before " + date.toString()
				+ " in a directory named: " + photo.getParentFile().getName() + ":\n";
		String logInfo2 = "Name before reverting: " + nameBefore + "\n";
		String logInfo3 = "Name after reverting: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Undo the name of a photo back to the latest name before current name and
	 * record that in the log if there exists a past name.
	 * 
	 * @param photo
	 *            the photo File to undo the name back to the latest name before
	 *            current name
	 * @param photoNode
	 *            the corresponding photo node to undo the name back to the
	 *            latest name before current name
	 * @throws FailToRenamePhotoFileException
	 */
	public void logUndoName(File photo, PhotoNode photoNode) throws FailToRenamePhotoFileException {
		// Keep track of the name before undoing.
		String nameBefore = photo.getName();

		// Undo the name for both File photo and corresponding photoNode if
		// possible. Otherwise record the exception in the log.
		try {
			ArrayList<Tag> originalTags = photoNode.getCurrPhotoName().getLstPhotoTags();
			photoNode.undoPhotoName();

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is actually done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				ArrayList<Tag> newTags = photoNode.getCurrPhotoName().getLstPhotoTags();
				updateTagManager(originalTags, newTags);
			} else {

				// Log the failure of renaming the File name and throw an
				// exception
				String msg = "Undoing name failed: cannot rename the photo, " + photo.getName() + ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}
		} catch (CannotUndoNameException e) {

			// Record the exception in log and don't execute further steps.
			String msg = "Undoing name failed: cannot undo name for photo: " + photo.getName()
					+ ", since there's no existing past name for this photo";
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the undoing of the name if no exception is thrown.
		String logInfo1 = "Undo name for a photo to its latest name before current one in a directory named: "
				+ photo.getParentFile().getName() + ":\n";
		String logInfo2 = "Name before undoing: " + nameBefore + "\n";
		String logInfo3 = "Name after undoing: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Update existingTags by removing tags in the collection originalTags, if a
	 * tag in originalTags neither still exist in newTags nor tagged to some
	 * photo in this PhotoManager.
	 * 
	 * @param originalTags
	 *            a collection of Tag as candidate to remove from the TagManager
	 *            for this PhotoManager
	 * @param newTags
	 *            a collection of Tag not to remove from the TagManager for this
	 *            PhotoManager if they show up in originalTags
	 */
	private void updateTagManager(ArrayList<Tag> originalTags, ArrayList<Tag> newTags) {
		// Loop over all Tag in originalTags.
		for (Tag t : originalTags) {

			// Check whether the candidate t to remove is protected in newTags.
			if (!newTags.contains(t)) {

				// Check whether t is tagged to some photo in this PhotoManager.
				ArrayList<Pair<File, PhotoNode>> temp = searchTag(flattenedPhotoCollection, t);
				if (temp.isEmpty()) {

					try {
						// Remove Tag t.
						existingTags.deleteTag(t);
					} catch (NotAnExistingTagException e) {
						e.printStackTrace();
					}
				}
			}
		}

		for (Tag t : newTags) {
			existingTags.addTag(t);
		}
	}

	/**
	 * Rename the File photo and its corresponding photoNode by adding a new tag
	 * and record that in the log. If the newTag is already a tag for the photo,
	 * don't change the current name of the node, but record the attempt of
	 * adding a duplicate tag.
	 * 
	 * @param photo
	 *            the photo File to rename by adding a tag
	 * @param photoNode
	 *            the corresponding photo node to rename by adding a tag
	 * @param newTag
	 *            the new tag to add
	 * @throws FailToRenamePhotoFileException
	 */
	public void logTagPhoto(File photo, PhotoNode photoNode, Tag newTag) throws FailToRenamePhotoFileException {
		// Keep track of the name before adding a tag.
		String nameBefore = photo.getName();

		// Tag photo for both the File and the Node if possible. Otherwise
		// record the exception in the log.
		try {

			// Tag the photo and update TagManager for this PhotoManager.
			photoNode.tagPhoto(newTag);

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is successfully done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				existingTags.addTag(newTag);
			} else {

				// Log the failure of renaming the File name and throw an
				// exception.
				String msg = "Tagging failed: cannot rename the photo, " + photo.getName() + ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}

		} catch (DuplicateTagException e) {

			// Record the attempt of adding a duplicate tag and stop the
			// execution of this method.
			String msg = "Tagging failed: cannot add duplicate tag for one photo. " + newTag.toString()
					+ " is already a tag for photo named: " + photo.getName();
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the adding of a new tag.
		String logInfo1 = "Add a new tag, " + newTag.toString() + ", for a photo in the directory named: "
				+ photo.getParentFile().getName() + ":\n";
		String logInfo2 = "Name before adding the tag: " + nameBefore + "\n";
		String logInfo3 = "Name after adding the tag: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Rename the File photo and its corresponding photoNode by adding a list of
	 * new tags from tagsToAdd and record that in the log. If the any tag in the
	 * list is already a tag for the photo, don't change the current name of the
	 * node, but record the attempt of adding a duplicate tag.
	 * 
	 * @param photo
	 *            the photo File to rename by adding a list of tags
	 * @param photoNode
	 *            the corresponding photo node to rename by adding a list of
	 *            tags
	 * @param tagsToAdd
	 *            a list of tags to add
	 * @throws FailToRenamePhotoFileException
	 */
	public void logTagPhotoByCollection(File photo, PhotoNode photoNode, ArrayList<Tag> tagsToAdd)
			throws FailToRenamePhotoFileException {
		// Keep track of the name before adding a tag.
		String nameBefore = photo.getName();

		// Tag photo for both the File and the Node if possible. Otherwise
		// record the exception in the log.
		try {

			// Tag the photo and update TagManager for this PhotoManager.
			photoNode.tagPhotoByCollection(tagsToAdd);

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is successfully done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				for (Tag tag : tagsToAdd) {
					existingTags.addTag(tag);
				}
			} else {

				// Log the failure of renaming the File name and throw an
				// exception.
				String msg = "Tagging a list of tags failed: cannot rename the photo, " + photo.getName()
						+ ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}

		} catch (DuplicateTagException e) {

			// Record the attempt of adding a duplicate tag and stop the
			// execution of this method.
			String msg = "Tagging a list of tags failed: cannot add duplicate tag for one photo. ";
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the adding of a new tag.
		String logInfo1 = "Add a list of tags to a photo in the directory named: " + photo.getParentFile().getName()
				+ ":\n";
		String logInfo2 = "Name before adding tags: " + nameBefore + "\n";
		String logInfo3 = "Name after adding tags: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Rename the File photo and its corresponding photoNode by removing an
	 * unwanted tag and record that in the log if that unwantedTag does exist in
	 * the current name.
	 * 
	 * @param photo
	 *            the photo File to rename by removing a tag
	 * @param photoNode
	 *            the corresponding photo node to rename by removing a tag
	 * @param unwantedTag
	 *            the unwanted tag to remove from the current name if here's
	 *            such a tag existing in the current name
	 * @throws FailToRenamePhotoFileException
	 */
	public void logDetagPhoto(File photo, PhotoNode photoNode, Tag unwantedTag) throws FailToRenamePhotoFileException {
		// Keep track of the name before removing a tag.
		String nameBefore = photo.getName();

		// Detag an unwanted tag for both the File and the Node if possible.
		// Otherwise record the exception in the log.
		try {

			// Detag the node.
			photoNode.detagPhoto(unwantedTag);

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is successfully done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				ArrayList<Tag> removeT = new ArrayList<Tag>();
				removeT.add(unwantedTag);
				ArrayList<Tag> protectT = new ArrayList<Tag>();
				updateTagManager(removeT, protectT);
			} else {

				// Log the failure of renaming the File name and throw an
				// exception.
				String msg = "Detagging failed: cannot rename the photo, " + photo.getName() + ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}

		} catch (NotAnExistingTagException e) {

			// Record the attempt of removing a not-existing tag and stop the
			// execution of this method.
			String msg = "Detagging failed: cannot detag tag, " + unwantedTag.toString() + ", for photo: "
					+ photo.getName() + ", since the tag doesn't exist in the current photo name.";
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the deleting of a tag if no exception is thrown.
		String logInfo1 = "Delete an unwanted tag, " + unwantedTag.toString() + ", for a photo in the directory named: "
				+ photo.getParentFile().getName() + ":\n";
		String logInfo2 = "Name before deleting the tag: " + nameBefore + "\n";
		String logInfo3 = "Name after deleting the tag: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Rename the File photo and its corresponding photoNode by removing a list
	 * of tags from tagsToRemove and record that in the log if that unwantedTag
	 * does exist in the current name.
	 * 
	 * @param photo
	 *            the photo File to rename by removing a list of tags
	 * @param photoNode
	 *            the corresponding photo node to rename by removing a list of
	 *            tags
	 * @param tagsToRemove
	 *            a list of tags to remove from the current name of photo if
	 *            here's such tags existing in the current name
	 * @throws FailToRenamePhotoFileException
	 */
	public void logDetagPhotoByCollection(File photo, PhotoNode photoNode, ArrayList<Tag> tagsToRemove)
			throws FailToRenamePhotoFileException {
		// Keep track of the name before removing a tag.
		String nameBefore = photo.getName();

		// Detag for both the File and the Node if possible.
		// Otherwise record the exception in the log.
		try {

			// Detag the node.
			photoNode.detagPhotoByCollection(tagsToRemove);

			// Keep track of the file we get after "renaming" to see whether the
			// renaming is successfully done or not
			File renamedPhotoFile = renamePhotoFile(photo, photoNode);
			if (!renamedPhotoFile.equals(photo)) {

				// Update the collection of photos, since File is immutable.
				updateFlattenedPhotoCollection(photo, photoNode, renamedPhotoFile);

				// Update TagManager.
				ArrayList<Tag> removeT = new ArrayList<Tag>();
				for (Tag tag : tagsToRemove) {
					removeT.add(tag);
				}
				ArrayList<Tag> protectT = new ArrayList<Tag>();
				updateTagManager(removeT, protectT);
			} else {

				// Log the failure of renaming the File name and throw an
				// exception.
				String msg = "Detagging a list of tags failed: cannot rename the photo, " + photo.getName()
						+ ", as a File.";
				logger.log(Level.INFO, msg);
				throw new FailToRenamePhotoFileException(msg);
			}

		} catch (NotAnExistingTagException e) {

			// Record the attempt of removing a not-existing tag and stop the
			// execution of this method.
			String msg = "Detagging a list of tags failed: cannot detag a list of tag for photo: " + photo.getName()
					+ ", since there's at least one tag to remove doesn't exist in the current photo name.";
			logger.log(Level.INFO, msg);
			return;
		}

		// Log the deleting of a tag if no exception is thrown.
		String logInfo1 = "Delete a list of tags for a photo in the directory named: " + photo.getParentFile().getName()
				+ ":\n";
		String logInfo2 = "Name before deleting the tag: " + nameBefore + "\n";
		String logInfo3 = "Name after deleting the tag: " + photoNode.getName();
		logger.log(Level.FINE, logInfo1 + logInfo2 + logInfo3);
	}

	/**
	 * Update a specific pair (oldPhotoFile, photoNode) to be (renamedPhotoFile,
	 * photoNode) in the flattenedPhotoCollection in this PhotoManager.
	 * 
	 * @param oldPhotoFile
	 *            the old photo File to be replaced
	 * @param renamedPhotoNode
	 *            the corresponding PhotoNode representing renamedPhotoFile
	 * @param renamedPhotoFile
	 *            the new photo File to set
	 */
	private void updateFlattenedPhotoCollection(File oldPhotoFile, PhotoNode renamedPhotoNode, File renamedPhotoFile) {
		// The new pair to replace the old one.
		Pair<File, PhotoNode> newPair = new Pair<File, PhotoNode>(renamedPhotoFile, renamedPhotoNode);

		// Loop over and find the index where the replacement happens.
		int index = 0;
		for (Pair<File, PhotoNode> photoPair : flattenedPhotoCollection) {
			if (photoPair.getKey().equals(oldPhotoFile)) {
				flattenedPhotoCollection.set(index, newPair);
				break;
			}
			index++;
		}
	}

	/**
	 * Return a list of 2-element pairs of (File photo, corresponding PhotoNode)
	 * for photos, which has been tagged a specific tag, in a list of 2-element
	 * pairs for (File photo, corresponding PhotoNode).
	 * 
	 * @param flattenedPhotos
	 *            a list of 2-element pairs for (File photo, corresponding
	 *            PhotoNode)
	 * @param aimTag
	 *            the tag to search for
	 * @return a list of 2-element pairs of (File photo, corresponding
	 *         PhotoNode) for photos containing the aimed tag
	 */
	public ArrayList<Pair<File, PhotoNode>> searchTag(ArrayList<Pair<File, PhotoNode>> flattenedPhotos, Tag aimTag) {
		// Construct an accumulator.
		// Loop over the passed-in collection and collect photo containing
		// aimTag.
		ArrayList<Pair<File, PhotoNode>> acc = new ArrayList<Pair<File, PhotoNode>>();
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {

			// If the photo we are currently looking at has been tagged the
			// aimTag, add that into the accumulator.
			ArrayList<Tag> tags = photoPair.getValue().getCurrPhotoName().getLstPhotoTags();
			if (tags.contains(aimTag)) {
				acc.add(photoPair);
			}
		}

		// If we are looking at a non-image photo, keep the accumulator empty.
		// Return the accumulator.
		return acc;
	}
}
