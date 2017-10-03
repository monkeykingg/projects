package model;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.util.ArrayList;
import java.util.Date;

import auxiliary.FailToRenamePhotoFileException;
import auxiliary.FileTypeException;
import auxiliary.NotAnExistingTagException;
import javafx.util.Pair;

public class Main {

	public static void main(String[] args)
			throws FileTypeException, ClassNotFoundException, IOException, NotAnExistingTagException, FailToRenamePhotoFileException {
//		File root = new File("/Users/Sangria/Desktop/test");
//		FileNode rootNode = new FileNode(root.getName(), null, FileType.DIRECTORY);
////		PhotoManager test = new PhotoManager(root, rootNode);
//		
//		PhotoRenamer test = new PhotoRenamer(root, rootNode);
//		
//		System.out.println(test.printTagSearch(new Tag("Painting")));
//		System.out.println(test.printTagSearch(new Tag("Jiu~")));
		
//		StringBuffer sb = new StringBuffer();
//		FileManager.buildDirectoryContents(test.getPhotoCabinet().getPhotoTree(), sb, "");
//		System.out.println(sb);
//		
//		String path = "/Users/Sangria/Desktop/test/Tags.ser";
//		// Read object
//		InputStream inputStream = new FileInputStream(path);
//		InputStream buffer = new BufferedInputStream(inputStream);
//		ObjectInput input = new ObjectInputStream(buffer);
//		TagManager tagManager = (TagManager) input.readObject();
//		
//		//close
//		input.close();
//		
//		System.out.println();
////		for (Tag t : tagManager.getCurrTags()){
////			System.out.println(t.toString());
////		}
//		System.out.println(test.listTags());
//		System.out.println();
//		System.out.println(test.getPhotoCabinet().getFlattenedPhotoCollection().isEmpty());
//		System.out.println(test.getPhotoCabinet().getFlattenedPhotoCollection().size());
//		System.out.println();
//
//		Tag newTag1 = new Tag("Errr");
//		Tag newTag2 = new Tag("HIiii");
//		Tag newTag3 = new Tag("Blaaa");
//		ArrayList<Tag> l = new ArrayList<Tag>();
//		l.add(newTag1);
//		l.add(newTag2);
//		l.add(newTag3);
//		
////		for (Pair<File, PhotoNode> photoPair : test.getPhotoCabinet().getFlattenedPhotoCollection()) {
////			test.getPhotoCabinet().logTagPhotoByCollection(photoPair.getKey(), photoPair.getValue(), l);
////		}
//		test.renameAllByCollection(l, 'A');
//		System.out.println("-------------------------------");
//		for (Pair<File, PhotoNode> c : test.getPhotoCabinet().getFlattenedPhotoCollection()) {
//			System.out.println(c.getKey().getName());
//			
//		}
//		System.out.println("-------------------------------");
//		System.out.println(test.listTags());
////		System.out.println(test.undoNameAll().toString());
////		
////		System.out.println("-------------------------------");
////		for (Pair<File, PhotoNode> c : test.getPhotoCabinet().getFlattenedPhotoCollection()) {
////			System.out.println(c.getKey().getName());
////			
////		}
////		System.out.println("-------------------------------");
//		
//		
//		System.out.println();
//		System.out.println();
//		Date date = new Date(1100, 10, 31);
//		System.out.println(test.revertAllNameByDate(date));
//		for (Pair<File, PhotoNode> c : test.getPhotoCabinet().getFlattenedPhotoCollection()) {
//			System.out.println(c.getKey().getName());
//		}
//		System.out.println(test.listTags());
//
////		System.out.println(test.undoNameAll());
//		
//		// Read object
//		InputStream inputStream2 = new FileInputStream(path);
//		InputStream buffer2 = new BufferedInputStream(inputStream2);
//		ObjectInput input2 = new ObjectInputStream(buffer2);
//		TagManager tagManager2 = (TagManager) input2.readObject();
//
//		// Close the stream
//		input2.close();
////		System.out.println();
////		for (Tag t : tagManager2.getCurrTags()){
////			System.out.println(t.toString());
////		}
////		System.out.println();
//		System.out.println(test.listTags());
//
////		// Test Photo Name
////		String s = "a @Happy haha @ blah *dasas @AUNT hello.jpg";
////		String ss = PhotoName.extractPlainNameWithoutTags(s);
////		System.out.println(ss);
////		String s1 = PhotoName.extractExtension(s);
////		System.out.println(s1);
////		String s2 = PhotoName.extractNameWithoutExtension(s);
////		System.out.println(s2);
////		ArrayList<Tag> ll = PhotoName.extractTags(s2);
////		for (Tag t : ll) {
////			System.out.println(t.toString());
////		}
////		String h = PhotoName.combineTags(ll);
////		System.out.println(h);
////		System.out.println(h.charAt(h.length() - 1));
////
		
		
		File root = new File("/Users/Sangria/Desktop/CDF test file/testDir");
		FileNode rootNode = new FileNode(root.getName(), null, FileType.DIRECTORY);		
		PhotoRenamer test = new PhotoRenamer(root, rootNode);
		
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.printPhotoTree());
		System.out.println("==============================================================");
		
		Pair<File, PhotoNode> choosedPhoto = test.choosePhoto("/Users/Sangria/Desktop/CDF test file/testDir/1 @Haha.jpg");
		test.rename(choosedPhoto.getKey(), choosedPhoto.getValue(), new Tag("Haha"), 'D');
		System.out.println();
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.listTags());
		System.out.println("==============================================================");
		
		Tag newTag1 = new Tag("A");
		Tag newTag2 = new Tag("B");
		Tag newTag3 = new Tag("C");
		ArrayList<Tag> l = new ArrayList<Tag>();
		l.add(newTag1);
		l.add(newTag2);
		l.add(newTag3);
		test.renameAllByCollection(l, 'A');
		System.out.println();
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.listTags());
		
		System.out.println("==============================================================");
		System.out.println(test.undoNameAll().toString());
		System.out.println();
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.listTags());

		System.out.println("==============================================================");
		Date date = new Date(1100, 10, 31);
		System.out.println(test.revertAllNameByDate(date));
		System.out.println();
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.listTags());
		
		System.out.println("==============================================================");
		Date date2 = new Date(10, 10, 31);
		System.out.println(test.revertAllNameByDate(date2));
		System.out.println();
		System.out.println(test.listPhotos());
		System.out.println();
		System.out.println(test.listTags());
	}

}
